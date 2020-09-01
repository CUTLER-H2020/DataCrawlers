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

This code is used to crawl/parse geo-data from shapefile.
By downloading this code, you agree to contact the corresponding data provider
and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process)
all data obtained from the data source.

"""

import fiona
import pyproj
import logging
import os
import json
from shapely.geometry import shape, mapping
from shapely.ops import transform
from kafka import KafkaProducer
from dotenv import load_dotenv

from constants import *


def generate_data(shp_file):
    with fiona.open(shp_file) as collection:

        has_shp_valid_geometries = True

        for feature in collection:
            # create a shape with the geometry and transform the coordinates (if needed)
            if feature['geometry']:
                geom = shape(feature['geometry'])
            else:
                continue

            if collection.crs['init'] != EPSG_TARGET:
                geom = apply_transformation(geom, collection.crs['init'])

            # check if geometry is valid
            if not geom.is_valid:
                has_shp_valid_geometries = False
                continue

            # the payload that will be populated
            body = {}

            body.update(feature['properties'])

            # add the remaining geometry
            body['geometry'] = mapping(geom)

            # Add class enumeration from classe field
            # for maps visualization reasons
            body['class'] = CLASS_ENUM.get(body['CLASSE'])

            # print(body)
            producer.send(KAFKA_TOPIC, body)

        if has_shp_valid_geometries:
            logger.error("File: {} has invalid geometries!".format(shp_file))


def apply_transformation(src_pol, crs):
    transformer = pyproj.Transformer.from_proj(pyproj.Proj(crs), pyproj.Proj(EPSG_TARGET), always_xy=True)
    des_pol = transform(transformer.transform, src_pol)

    return des_pol


load_dotenv()

logging.basicConfig(filename="error.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.ERROR)

producer = KafkaProducer(bootstrap_servers=["{}:{}".format(os.getenv('KAFKA_HOST'), os.getenv('KAFKA_PORT'))],
                         security_protocol=os.getenv('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT'),
                         ssl_cafile=os.getenv('KAFKA_CA_FILE', None),
                         ssl_certfile=os.getenv('KAFKA_CERT_FILE', None),
                         ssl_keyfile=os.getenv('KAFKA_KEY_FILE', None),
                         value_serializer=lambda m: json.dumps(m).encode('utf8'))

print("Processing...")
generate_data(SHP_FILE)
print("Done")

# Make the assumption that all messages are published and consumed
producer.send(KAFKA_TOPIC_FINISH, 'All messages are published and consumed successfully!')
producer.flush()
