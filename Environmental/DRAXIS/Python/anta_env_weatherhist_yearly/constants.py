KAFKA_TOPIC = 'ANTA_ENV_WEATHERHIST_YEARLY'
KAFKA_TOPIC_FINISH = 'ANTA_ENV_WEATHERHIST_FINISH_YEARLY'

ELASTICSEARCH_INDEX = "anta_env_weatherhist_yearly"

BBOX_CSV = "20.0,-10.0,75.0,45.0"

STARTING_DATE = '2010-01-01'

CORK_LAT = 36.963974
CORK_LON = 30.727117

INDEX_METADATA_MAPPING = {
    'temp-avg': {'description': 'Temperature [°C]', 'unit': '°C'},
    'wind': {'description': 'Wind speed [m/s]', 'unit': 'm/s'},
    'rh': {'description': 'Relative humidity [%]', 'unit': '%'},
    'total-prec': {'description': 'Total precipitation [kg/m^2]', 'unit': 'kg/m^2'}
}

WIND_X_AXIS_VARIABLE = 'u10'
WIND_Y_AXIS_VARIABLE = 'v10'


class ClimatologyException(Exception):
    pass
