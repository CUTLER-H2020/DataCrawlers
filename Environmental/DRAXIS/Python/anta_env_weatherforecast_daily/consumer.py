import os
import json
from kafka import KafkaConsumer
from elastic import ElasticSearchClient
from dotenv import load_dotenv
from constants import *


def insert_modified_data(forecast):
    # Add the special character to temperature for Kibana visualization reasons
    forecast['temperature2m']['unit'] = "°C"
    forecast['temperature2m']['description'] = "Temperature [°C]"

    for variable, data in forecast.items():
        doc = {"Variable": variable}
        for time, value in data['data'].items():
            doc['Date'] = time
            doc['Value'] = value

            doc['Unit'] = data['unit']
            doc['Description'] = data['description']
            doc['location'] = {
                'lat': ANTA_LAT,
                'lon': ANTA_LON
            }

            id_ = variable + time
            res = es.insert_doc(doc, id_=id_)
            print(res)


# Load environment variables
load_dotenv()

es = ElasticSearchClient(os.getenv('ES_HOST'), os.getenv('ES_PORT'),
                         use_ssl=os.getenv('ES_USE_SSL', False),
                         verify_certs=os.getenv('ES_VERIFY_CERTS', False),
                         http_auth=(os.getenv('ES_USER'), os.getenv('ES_PASSWORD')) if os.getenv('ES_USER') else None,
                         ca_certs=os.getenv('ES_CA_CERTS', None))

geo_point_mapping = es.define_geo_point_mapping()

es.create_index(ELASTICSEARCH_INDEX, geo_point_mapping)

kafka_consumer = KafkaConsumer(KAFKA_TOPIC,
                               bootstrap_servers=["{}:{}".format(os.getenv('KAFKA_HOST'), os.getenv('KAFKA_PORT'))],
                               # auto_offset_reset='earliest',
                               security_protocol=os.getenv('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT'),
                               ssl_cafile=os.getenv('KAFKA_CA_FILE', None),
                               ssl_certfile=os.getenv('KAFKA_CERT_FILE', None),
                               ssl_keyfile=os.getenv('KAFKA_KEY_FILE', None),
                               group_id='group_' + KAFKA_TOPIC,
                               value_deserializer=lambda m: json.loads(m.decode('utf8')))

for msg in kafka_consumer:
    insert_modified_data(msg.value)

