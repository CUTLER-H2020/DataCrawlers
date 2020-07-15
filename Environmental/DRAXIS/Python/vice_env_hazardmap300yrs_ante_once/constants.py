import logging

KAFKA_TOPIC = 'VICE_ENV_HAZARDMAP_300YRS_ANTE_ONCE'
KAFKA_TOPIC_FINISH = 'VICE_ENV_HAZARDMAP_300YRS_ANTE_FINISH_ONCE'

ELASTICSEARCH_INDEX = 'vice_env_hazardmap300yrs_ante_once'

SHP_FILE = "shapefile/reprojected/HAZARD_MAP_WL_TR300_ANTE_OPERAM.shp"

EPSG_TARGET = 'epsg:4326'

logging.basicConfig(filename="error.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.ERROR)

logger = logging.getLogger(__name__)
