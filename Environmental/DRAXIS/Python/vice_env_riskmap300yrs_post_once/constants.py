import logging

KAFKA_TOPIC = 'VICE_ENV_RISKMAP_300YRS_POST_ONCE'
KAFKA_TOPIC_FINISH = 'VICE_ENV_RISKMAP_300YRS_POST_FINISH_ONCE'

ELASTICSEARCH_INDEX = 'vice_env_riskmap300yrs_post_once'

SHP_FILE = "shapefile/reprojected/RISK_MAP_TR300_POST_OPERAM.shp"

EPSG_TARGET = 'epsg:4326'

logging.basicConfig(filename="error.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.ERROR)

logger = logging.getLogger(__name__)

CLASS_ENUM = {
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4
}
