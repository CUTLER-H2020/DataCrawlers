import logging

KAFKA_TOPIC = 'VICE_ENV_DISCONT_ONCE'
KAFKA_TOPIC_FINISH = 'VICE_ENV_DISCONT_FINISH_ONCE'

ELASTICSEARCH_INDEX = 'vice_env_discont_once'

SHP_DIR = "shapefiles"

EPSG_TARGET = 'epsg:4326'

logging.basicConfig(filename="error.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.ERROR)

logger = logging.getLogger(__name__)
