import os
import json
import requests
import datetime
from kafka import KafkaProducer
from dotenv import load_dotenv
from constants import *
from elastic import ElasticSearchClient

"""
The way this producer works is that it checks the number of docs in Elastic about the index "thess_env_airquality_daily"
If it isn't equal to 0 that means it's already populated with historical data. So broadcast only latest data
If it is 0, populates it with all historical data.

"""


def get_historical_air_quality_measurements(station_id):
    headers = {
        'Key': os.getenv("AQ_HUB_KEY")
    }

    url = "{}/v2/stations/{}/measurements".format(os.getenv("AQ_HUB_URL"),
                                                  station_id)

    response = requests.get(url=url, headers=headers)
    res = response.json()

    # from response we just want the "data" part containing the pollutant values
    return res['data']


def get_latest_air_quality_measurements(station_id):
    # The response data from "/last_measurements" endpoint differ from "/measurements"
    # It includes more data, and has a different key at json, for representing the date
    skeleton = {
        "t": None,
        "CO": None,
        "NO2": None,
        "O3": None,
        "PM10": None,
        "PM25": None,
        "SO2": None
    }

    headers = {
        'Key': os.getenv("AQ_HUB_KEY")
    }

    url = "{}/v2/stations/{}/last_measurements".format(os.getenv("AQ_HUB_URL"),
                                                       station_id)

    response = requests.get(url=url, headers=headers)
    res = response.json()

    data = res['data'][0]

    time = data['last_measurement_at']
    data['t'] = time
    for key in skeleton.keys():
        skeleton[key] = data.get(key)

    return skeleton


def produce_historical_data():
    # Here we get data about a bunch of days with a defined schema
    # exactly how AQHub's response data are, at "/measurements" endpoint
    for station_name, station_id in STATIONS_ID.items():
        station_data = get_historical_air_quality_measurements(station_id)
        for day in station_data:
            broadcast_data(day, station_name)


def produce_latest_data():
    # Here we get data for one day only (last day we had a measurement) with a defined schema
    # exactly how AQHub's response data are, at "/measurements" endpoint
    for station_name, station_id in STATIONS_ID.items():
        last_day = get_latest_air_quality_measurements(station_id)
        broadcast_data(last_day, station_name)


def daily_aqi(pm10):
    """
    Function that uses an equation to compute daily AQI
    and returns a dict containing the value and
    the characterisation based on PM10 pollutant

    """
    if pm10 is None:
        return {
            "aqi_value": None,
            "aqi_characterisation": None
        }

    for bp_range in BREAKPOINTS_AQI.keys():
        bp_low = bp_range[0]
        bp_high = bp_range[1]
        if bp_low <= pm10 <= bp_high:
            i_low = BREAKPOINTS_AQI[bp_range]['i_low']
            i_high = BREAKPOINTS_AQI[bp_range]['i_high']

            aqi_value = ((i_high - i_low) / (bp_high - bp_low)) * (pm10 - bp_low) + i_low
            aqi_characterisation = BREAKPOINTS_AQI[bp_range]['characterisation']

            return {
                "aqi_value": aqi_value,
                "aqi_characterisation": aqi_characterisation
            }


def broadcast_data(day: dict, station_name: str):
    # Each day contains 6 pollutants,
    # for Kibana-reasons we need to broadcast only one pollutant under "Parameter" with it's according "Value"

    payload = {}
    internal_sent_messages = 0

    # '2020-03-18 10:30:02' is transformed to '2020-03-18'T'10:30:02'
    # thus Kibana automatically recognize it as a Date field
    time = day.pop('t')
    date_object = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    date = date_object.isoformat()

    # Add also a year field for Kibana-reasons
    year = date_object.year.__str__()

    # update all the day, with the dict of aqi_value and aqi_characterisation for all pollutants based on PM10
    pm10 = float(day['PM10']) if day['PM10'] is not None else None
    payload.update(daily_aqi(pm10))

    for pollutant, value in day.items():
        payload['Date'] = date
        payload['year'] = year

        payload['Parameter'] = pollutant
        payload['Parameter_fullname'] = POLLUTANTS_FULLNAME[pollutant]

        # AQHub measures pollutants values as strings instead of float
        payload['Value'] = float(value) if value is not None else None

        # handcraft location field, to be recognized as geo_point, ready for ES insertion
        payload['location'] = {
            'lat': STATIONS_LOCATION[station_name][0],
            'lon': STATIONS_LOCATION[station_name][1]
        }

        payload['station_name'] = station_name

        print(payload)
        producer.send(KAFKA_TOPIC, payload).get(10)

        internal_sent_messages += 1

    return internal_sent_messages


load_dotenv()

producer = KafkaProducer(bootstrap_servers=["{}:{}".format(os.getenv('KAFKA_HOST'), os.getenv('KAFKA_PORT'))],
                         security_protocol=os.getenv('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT'),
                         ssl_cafile=os.getenv('KAFKA_CA_FILE', None),
                         ssl_certfile=os.getenv('KAFKA_CERT_FILE', None),
                         ssl_keyfile=os.getenv('KAFKA_KEY_FILE', None),
                         value_serializer=lambda m: json.dumps(m).encode('utf8'))

es = ElasticSearchClient(os.getenv('ES_HOST'), os.getenv('ES_PORT'),
                         use_ssl=os.getenv('ES_USE_SSL', False),
                         verify_certs=os.getenv('ES_VERIFY_CERTS', False),
                         http_auth=(os.getenv('ES_USER'), os.getenv('ES_PASSWORD')) if os.getenv('ES_USER') else None,
                         ca_certs=os.getenv('ES_CA_CERTS', None))

if es.es.count(index=ELASTICSEARCH_INDEX)['count'] != 0:
    produce_latest_data()
else:
    produce_historical_data()

# Make the assumption that all messages are published and consumed
producer.send(KAFKA_TOPIC_FINISH, 'All messages are published and consumed successfully!')
producer.flush()
