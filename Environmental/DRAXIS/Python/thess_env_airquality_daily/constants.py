KAFKA_TOPIC = 'THESS_ENV_AIRQUALITY_DAILY'
KAFKA_TOPIC_FINISH = 'THESS_ENV_AIRQUALITY_FINISH_DAILY'

ELASTICSEARCH_INDEX = "thess_env_airquality_daily"

STATIONS_ID = {
    'New City Hall': '1',
    'Eptapyrgioy': '224',
    'Egnatias': '10421',
    'Martioy': '10517',
    'Lagkada': '10532',
    'Malakopi': '10533',
}

# Locations in (lat, lon format)
STATIONS_LOCATION = {
    'New City Hall': (40.623742, 22.954063),
    'Eptapyrgioy': (40.644223, 22.958404),
    'Egnatias': (40.637634, 22.94112),
    'Martioy': (40.60121, 22.960542),
    'Lagkada': (40.65228, 22.934897),
    'Malakopi': (40.616145, 22.982011),
}

POLLUTANTS_FULLNAME = {
    "CO": "Carbon monoxide (µg/m³)",
    "NO2": "Nitrogen dioxide (µg/m³)",
    "O3": "Ozone (µg/m³)",
    "PM10": "Particulate Matter, diameter less than 10 mm (µg/m³)",
    "PM25": "Particulate Matter, diameter less than 2.5 mm (µg/m³)",
    "SO2": "Sulphur dioxide (µg/m³)"
}

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
