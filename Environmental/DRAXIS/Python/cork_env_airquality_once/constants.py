KAFKA_TOPIC = 'CORK_ENV_AIRQUALITY_ONCE'
KAFKA_TOPIC_FINISH = 'CORK_ENV_AIRQUALITY_FINISH_ONCE'

ELASTICSEARCH_INDEX = "cork_env_airquality_once"

EXCEL_FILE = 'cork-airquality_public.xlsx'

STATION_NAME = "Pier Monitoring station"

STATION_LAT = 51.810327
STATION_LON = -8.278933

COLUMN_NAMES = [
    "Date",
    "SO2 (µg/m³)",
    "PM10 (µg/m³)",
    "PM25 (µg/m³)",
    "CO (µg/m³)",
    "NO (µg/m³)",
    "NO2 (µg/m³)",
    "O3 (µg/m³)"
]

# COLUMN_NAMES = ['date', 'so', 'pm10', 'pm25', 'co', 'no', 'no2', 'o3']

# Keep in mind that range(0,54) is 0...53
# so for example for the first case 0-54 use range(0,55)

BREAKPOINTS_AQI = {
    # 0-54
    (0, 54): {'i_low': 0, 'i_high': 50, 'characterisation': 'Good'},
    # 55-154
    (55, 154): {'i_low': 51, 'i_high': 100, 'characterisation': 'Moderate'},
    # 155-254
    (155, 254): {'i_low': 101, 'i_high': 150, 'characterisation': 'Unhealthy for Sensitive Groups'},
    # 255-354
    (255, 354): {'i_low': 151, 'i_high': 200, 'characterisation': 'Unhealthy'},
    # 355-424
    (355, 424): {'i_low': 201, 'i_high': 300, 'characterisation': 'Very Unhealthy'},
    # 425-504
    (425, 504): {'i_low': 301, 'i_high': 400, 'characterisation': 'Hazardous'},
    # 505-604
    (505, 604): {'i_low': 401, 'i_high': 500, 'characterisation': 'Hazardous'}
}
