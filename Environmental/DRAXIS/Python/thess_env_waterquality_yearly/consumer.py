import os
import json
from kafka import KafkaConsumer
from elastic import ElasticSearchClient
from dotenv import load_dotenv
from constants import *


def transform_message_for_es(msg: dict) -> dict:
    # the skeleton payload to insert data in Elasticsearch.
    # this will be updated with new values if exist.
    # thus when we won't have empty fields.
    send = {
        "Station": None,
        "Parameter": None,
        "Value": None,
        "location": None,
        "date": None,
        "Parameter_fullname": None,
        "Location": None,
        "Unit": None
    }

    lat = msg.pop('lat')
    lon = msg.pop('lon')

    msg['location'] = {
        'lat': lat,
        'lon': lon
    }

    send.update(msg)
    print(send)
    return send


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

c = 0
for msg in kafka_consumer:
    c += 1
    print("Consumed: {} messages".format(c))
    formatted_msg = transform_message_for_es(msg.value)
    es.insert_doc(formatted_msg)
