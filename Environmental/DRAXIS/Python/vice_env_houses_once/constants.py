import logging

KAFKA_TOPIC = 'VICE_ENV_HOUSES_ONCE'
KAFKA_TOPIC_FINISH = 'VICE_ENV_HOUSES_ONCE'

ELASTICSEARCH_INDEX = 'vice_env_houses_once'

SHP_FILE = "shapefile/reprojected/houses.shp"

EPSG_TARGET = 'epsg:4326'

logging.basicConfig(filename="error.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.ERROR)

logger = logging.getLogger(__name__)
