import logging

KAFKA_TOPIC = 'VICE_ENV_WALLS_ONCE'
KAFKA_TOPIC_FINISH = 'VICE_ENV_WALLS_ONCE'

ELASTICSEARCH_INDEX = 'vice_env_walls_once'

SHP_DIR = "shapefiles"

EPSG_TARGET = 'epsg:4326'

logging.basicConfig(filename="error.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.ERROR)

logger = logging.getLogger(__name__)
