import datetime

ANTA_LAT = 36.963974
ANTA_LON = 30.727117
ANTA_RESOLUTION = "18km"
FROM_DATE = datetime.datetime.now().strftime("%Y-%m-%d")
TO_DATE = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%Y-%m-%d")  # TO_DATE = FROM_DATE + 7 days
VARIABLES = ["temperature2m", "rh2m", "windspeed10m", "precipitation"]
TIMEZONE = "Europe/Athens"

KAFKA_TOPIC = 'ANTA_ENV_WEATHERFORECAST_DAILY'
KAFKA_TOPIC_FINISH = 'ANTA_ENV_WEATHERFORECAST_FINISH_DAILY'

ELASTICSEARCH_INDEX = 'anta_env_weatherforecast_daily'
