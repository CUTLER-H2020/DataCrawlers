"""
This code is open-sourced software licensed under the MIT license. (http://opensource.org/licenses/MIT)

Copyright 2020 Stergios Bampakis, DRAXIS ENVIRONMENTAL S.A.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

DISCLAIMER

This code is used to crawl/parse data from file from Cork Municipality (EPA_TRaCData_CorkHarbour_2010_2018 - ΕΝ_public.xlsx).
By downloading this code, you agree to contact the corresponding data provider
and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process)
all data obtained from the data source.

"""

import os
import json
from kafka import KafkaConsumer
from elastic import ElasticSearchClient
from dotenv import load_dotenv
from constants import *


def transform_message_for_es(msg: dict) -> dict:
    modified_msg = {}
    # Handcraft the parameter and value extraction from pollutant
    for pollutant in POLLUTANTS:
        if pollutant in msg:
            pollutant_name = pollutant
            pollutant_value = msg.pop(pollutant)

            modified_msg = msg.copy()

            # Delete fields we don't want to insert to ES
            modified_msg.pop('Dec_Lat')
            modified_msg.pop('Dec_Long')

            modified_msg['parameter'] = pollutant_name
            modified_msg['value'] = pollutant_value

    # Handcraft the location for geo point
    if msg["Dec_Lat"] is not None:
        lat_value = msg.pop("Dec_Lat")
    else:
        lat_value = None
    if msg["Dec_Long"] is not None:
        lon_value = msg.pop("Dec_Long")
    else:
        lon_value = None

    if (lat_value is not None) and (lon_value is not None):
        modified_msg['location'] = {"lat": lat_value, "lon": lon_value}
    else:
        modified_msg['location'] = None

    # Handcraft and integrate Date and Time
    modified_msg['Date'] += 'T' + modified_msg['Time'] if modified_msg['Time'] is not None else ""

    print(modified_msg)
    return modified_msg


load_dotenv()

es = ElasticSearchClient(os.getenv('ES_HOST'), os.getenv('ES_PORT'),
                         use_ssl=os.getenv('ES_USE_SSL', False),
                         verify_certs=os.getenv('ES_VERIFY_CERTS', False),
                         http_auth=(os.getenv('ES_USER'), os.getenv('ES_PASSWORD')) if os.getenv('ES_USER') else None,
                         ca_certs=os.getenv('ES_CA_CERTS', None))

geo_point_mapping = es.define_geo_point_mapping()

date_mapping = es.define_date_mapping()

es.create_index(ELASTICSEARCH_INDEX, geo_point_mapping, date_mapping)

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
    print(msg.value)
    print("Consumed: {} messages".format(c))
    formatted_msg = transform_message_for_es(msg.value)
    es.insert_doc(formatted_msg)
