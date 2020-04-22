import datetime

CORK_LAT = 51.804819
CORK_LON = -8.301993
CORK_RESOLUTION = "18km"
FROM_DATE = datetime.datetime.now().strftime("%Y-%m-%d")
TO_DATE = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%Y-%m-%d")  # TO_DATE = FROM_DATE + 7 days
VARIABLES = ["temperature2m", "rh2m", "windspeed10m", "precipitation"]
TIMEZONE = "Europe/Athens"

KAFKA_TOPIC = 'CORK_ENV_WEATHERFORECAST_DAILY'
KAFKA_TOPIC_FINISH = 'CORK_ENV_WEATHERFORECAST_FINISH_DAILY'

ELASTICSEARCH_INDEX = "cork_env_weatherforecast_daily"
