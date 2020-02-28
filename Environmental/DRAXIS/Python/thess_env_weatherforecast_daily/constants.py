import datetime

THESS_LAT = 40.607467
THESS_LON = 22.945836
THESS_RESOLUTION = "6km"
FROM_DATE = datetime.datetime.now().strftime("%Y-%m-%d")
TO_DATE = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%Y-%m-%d")  # TO_DATE = FROM_DATE + 7 days
VARIABLES = ["temperature2m", "rh2m", "windspeed10m", "precipitation"]
TIMEZONE = "Europe/Athens"

KAFKA_TOPIC = 'THESS_ENV_WEATHERFORECAST_DAILY'
KAFKA_TOPIC_FINISH = 'THESS_ENV_WEATHERFORECAST_FINISH_DAILY'

ELASTICSEARCH_INDEX = "thess_env_weatherforecast_daily"
