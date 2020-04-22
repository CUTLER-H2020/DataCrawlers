import os
import json
from kafka import KafkaConsumer
from elastic import ElasticSearchClient
from dotenv import load_dotenv
from constants import *


load_dotenv()

es = ElasticSearchClient(os.getenv('ES_HOST'), os.getenv('ES_PORT'),
                         use_ssl=os.getenv('ES_USE_SSL', False),
                         verify_certs=os.getenv('ES_VERIFY_CERTS', False),
                         http_auth=(os.getenv('ES_USER'), os.getenv('ES_PASSWORD')) if os.getenv('ES_USER') else None,
                         ca_certs=os.getenv('ES_CA_CERTS', None))

# We don't need a location field in this index
# geo_point_mapping = es.define_geo_point_mapping()

# this particular index should follow the previous index's
# format time which is "2017/01/01 00:15:00"
# instead of "2017/01/01T00:15:00" we're having it in all of our new indices
# So apply an explicit mapping for the field 'date'

date_mapping = es.define_custom_date_mapping_format(date_field_name='date', format="yyyy/MM/dd HH:mm:ss")

es.create_index(ELASTICSEARCH_INDEX, date_mapping)

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
    # Data are ready to be inserted to ES from producer.

    # Insert documents, with id's route_name+date eg. "Benizelou2020-04-09 16:15:00"
    # in order to avoid duplicate records
    doc = msg.value

    time = doc['date']
    route_name = doc['name']

    id_ = route_name + time

    print("Inserting doc: {}".format(doc))
    print("with id: {}".format(id_))

    result = es.insert_doc(doc_=doc, id_=id_)
    print("Status: {}".format(result))
