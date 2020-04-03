KAFKA_TOPIC = 'THESS_ENV_SPEEDMEASUREMENTS_15MIN'
KAFKA_TOPIC_FINISH = 'THESS_ENV_SPEEDMEASUREMENTS_FINISH_15MIN'

ELASTICSEARCH_INDEX = 'cutler_thess_speedmeasurements_1'

# INITIAL_VIEWSTATE = "/wEPDwUKMTc0NzQyOTQ5OA9kFgICAQ9kFgICAQ9kFgJmD2QWAgIJDxAPFgIeB0NoZWNrZWRoZGRkZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAQURTG9naW4xJFJlbWVtYmVyTWWh7E+yuILEH6P7p9tVx0NTPBpWPSubky7Jd64dHRgq0w=="

LOGIN_URL = "https://www.trafficthessreports.imet.gr/user_login.aspx?ReturnUrl=export.aspx"

BASE_URL = "https://www.trafficthessreports.imet.gr"


ROUTE_IDS = {
    "Egnatia (Syntribani - Plateia Dhmokratias)": 1,
    "Egnatia (Plateia Dhmokratias - Syntribani)": 2,
    "Dragoumh": 8,
    "Benizelou": 9
}


class ThessImetException(Exception):
    pass
