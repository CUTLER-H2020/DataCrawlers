import os
import json
import requests
from kafka import KafkaProducer
from dotenv import load_dotenv
from constants import *


def get_seven_day_forecast():
    """
    Method that issues request to DRAXIS API for the seven day forecast.
    Check for more info: https://api.draxis.gr/#weather-hourly-data

    Returns:
        dict: The response data of the forecast.

    """

    params = {
        "lat": ANTA_LAT,
        "lon": ANTA_LON,
        "resolution": ANTA_RESOLUTION,
        "from_date": FROM_DATE,
        "to_date": TO_DATE,
        "variables": ','.join(VARIABLES),
        # "timezone": TIMEZONE,
        "apikey": os.getenv("API_KEY")
    }

    url = os.getenv("DRAXIS_API_WEATHER_FORECAST_URL")
    response = requests.get(url=url, params=params)

    return response.json()


# Load environment variables
load_dotenv()

producer = KafkaProducer(bootstrap_servers=["{}:{}".format(os.getenv('KAFKA_HOST'), os.getenv('KAFKA_PORT'))],
                         security_protocol=os.getenv('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT'),
                         ssl_cafile=os.getenv('KAFKA_CA_FILE', None),
                         ssl_certfile=os.getenv('KAFKA_CERT_FILE', None),
                         ssl_keyfile=os.getenv('KAFKA_KEY_FILE', None),
                         value_serializer=lambda m: json.dumps(m).encode('utf8'))


# Get the seven days forecast
forecast = get_seven_day_forecast()

producer.send(KAFKA_TOPIC, forecast)

# Make the assumption that all messages are published and consumed
producer.send(KAFKA_TOPIC_FINISH, 'All messages are published and consumed successfully!')

producer.flush()
