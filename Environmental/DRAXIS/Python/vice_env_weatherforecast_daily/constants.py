import datetime

VICE_LAT = 45.548831
VICE_LON = 11.545437
VICE_RESOLUTION = "6km"
FROM_DATE = datetime.datetime.now().strftime("%Y-%m-%d")
TO_DATE = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%Y-%m-%d")  # TO_DATE = FROM_DATE + 7 days
VARIABLES = ["temperature2m", "rh2m", "windspeed10m", "precipitation"]
TIMEZONE = "Europe/Athens"

KAFKA_TOPIC = 'VICE_ENV_WEATHERFORECAST_DAILY'
KAFKA_TOPIC_FINISH = 'VICE_ENV_WEATHERFORECAST_FINISH_DAILY'

ELASTICSEARCH_INDEX = "vice_env_weatherforecast_daily"
