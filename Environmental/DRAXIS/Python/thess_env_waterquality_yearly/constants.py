KAFKA_TOPIC = 'THESS_ENV_WATERQUALITY_YEARLY'
KAFKA_TOPIC_FINISH = 'THESS_ENV_WATERQUALITY_FINISH_YEARLY'

ELASTICSEARCH_INDEX = 'thess_env_waterquality_yearly'

# Mapping the stations to Lat, Lon
# This applies to all excel files since they look alike
STATIONS = {
    "SP1": (40.5870417, 22.9163638),
    "SP2": (40.5896583, 22.8727694),
    "SP3": (40.6126111, 22.8654027),
    "SP4": (40.6332222, 22.8963666),
    "SP5": (40.6118028, 22.9065916),
    "LP2": (40.6348861, 22.9263444),
    "ARISTOTELOUS": (40.6320472, 22.9399888),
    "LP3": (40.6177694, 22.9511555),
    "LP4": (40.5952333, 22.9478722),
    "LP5": (40.5931417, 22.9473277)
}

STATIONS_LOCATIONS = {
    'LP2': 'LIMANI',
    'ARISTOTELOUS': 'ARISTOTELOUS',
    'LP3': 'MAK PALLAS',
    'LP4': 'MEGARO',
    'LP5': 'KELLARIOS'
}

PARAMETERS_FULLNAME_MAPPING = {
    'Depth (m)': 'Depth of sample (m)',
    'Tv290C': 'Temperature (°C)',
    'Sal00': 'Salinity (PSU)',
    'C0S/m': 'Conductivity (S/m)',
    'Secchi (m)': 'Secchi Depth (m)',
    'pH': None,
    'DO (%)': 'Dissolved Oxygen (%)',
    'DO (mg/L)': 'Dissolved Oxygen (mg/L)'
}

PARAMETERS_UNIT_MAPPING = {
    'Depth (m)': 'm',
    'Tv290C': '°C',
    'Sal00': 'PSU',
    'C0S/m': 'S/m',
    'Secchi (m)': 'm',
    'pH': None,
    'DO (%)': '%',
    'DO (mg/L)': 'mg/L'
}

# Constants to be used for scraping 2016 data
EXCEL_2016 = "2016_CTDatAl_public.xlsx"
MONTHS_SHEETS_2016 = ['IAN16', 'FEB16', 'MARCH16', 'APRIL16', 'MAY16', 'JUL16', 'JUN16', 'AUG16', 'SEPT16', 'OKT16', 'NOE16', 'DEC16']
DATES_2016_MAPPING = {
    'IAN16': "2016-01-01",
    'FEB16': "2016-02-01",
    'MARCH16': "2016-03-01",
    'APRIL16': "2016-04-01",
    'MAY16': "2016-05-01",
    'JUN16': "2016-06-01",
    'JUL16': "2016-07-01",
    'AUG16': "2016-08-01",
    'SEPT16': "2016-09-01",
    'OKT16': "2016-10-01",
    'NOE16': "2016-11-01",
    'DEC16': "2016-12-01"
}


# Constants to be used for scraping 2017 data
EXCEL_2017 = "2017_CTDatAl_public.xlsx"
MONTHS_SHEETS_2017 = ['IAN17', 'FEV17', 'MAR17', 'APRIL17', 'MAY17', 'JUN17', 'JUL17', 'AUG17', 'SEPT17', 'OKT17']
DATES_2017_MAPPING = {
    'IAN17': "2017-01-01",
    'FEV17': "2017-02-01",
    'MAR17': "2017-03-01",
    'APRIL17': "2017-04-01",
    'MAY17': "2017-05-01",
    'JUN17': "2017-06-01",
    'JUL17': "2017-07-01",
    'AUG17': "2017-08-01",
    'SEPT17': "2017-09-01",
    'OKT17': "2017-10-01"
}

# Constants to be used for scraping 2018 data
EXCEL_2018 = "2018_CTDatAl_public.xlsx"
MONTHS_SHEETS_2018 = ['IOUL18', 'AUG18', 'SEPT18', 'OKT18', 'NOE18', 'DEC18']
DATES_2018_MAPPING = {
    'IOUL18': "2018-07-01",
    'AUG18': "2018-08-01",
    'SEPT18': "2018-09-01",
    'OKT18': "2018-10-01",
    'NOE18': "2018-11-01",
    'DEC18': "2018-12-01"
}

# Constants to be used for scraping 2019 data
EXCEL_2019 = "2019_CTDatAl_public.xlsx"
MONTHS_SHEETS_2019 = ['IAN19', 'FEV19', 'MART19', 'APRIL19', 'MAY19', 'JUN19', 'JUL19']
DATES_2019_MAPPING = {
    'IAN19': "2019-01-01",
    'FEV19': "2019-02-01",
    'MART19': "2019-03-01",
    'APRIL19': "2019-04-01",
    'MAY19': "2019-05-01",
    'JUN19': "2019-06-01",
    'JUL19': "2019-07-01"
}
