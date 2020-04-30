KAFKA_TOPIC = 'THESS_ENV_WATERQUALITY_CHLOR_YEARLY'
KAFKA_TOPIC_FINISH = 'THESS_ENV_WATERQUALITY_CHLOR_FINISH_YEARLY'

ELASTICSEARCH_INDEX = 'thess_env_waterquality_chlor_yearly'

EXCEL_FILE = "Chlorophyll_2014_2019_public.xlsx"

FIRST_LP_SHEET = "LP_Chl-a"

SECOND_SP_SHEET = "SP_Chl-a"

# Mapping the stations to Lat, Lon
STATIONS = {
    "SP1": (40.5870417, 22.9163638),
    "SP2": (40.5896583, 22.8727694),
    "SP3": (40.6126111, 22.8654027),
    "SP4": (40.6332222, 22.8963666),
    "SP5": (40.6118028, 22.9065916),
    # There is no mention for the coords of LP1, this coords are found by searching the name of the station ΚΑΛΟΧΩΡΙ
    "LP1": (40.640872, 22.856316),
    "LP2": (40.6348861, 22.9263444),
    # In this file ARISTOTELOUS stations is referenced as ARIST
    "ARIST": (40.6320472, 22.9399888),
    "LP3": (40.6177694, 22.9511555),
    "LP4": (40.5952333, 22.9478722),
    "LP5": (40.5931417, 22.9473277)
}

