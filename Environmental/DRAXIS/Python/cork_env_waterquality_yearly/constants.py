KAFKA_TOPIC = 'CORK_ENV_WATERQUALITY_YEARLY'
KAFKA_TOPIC_FINISH = 'CORK_ENV_WATERQUALITY_FINISH_YEARLY'

ELASTICSEARCH_INDEX = 'cork_env_waterquality_yearly'

EXCEL_FILE = "EPA_TRaCData_CorkHarbour_2010_2018 - ΕΝ_public.xlsx"

SHEET1 = "Stations"
COLUMNS1 = ["WB_Name",
            "Station_No",
            "Location",
            "WB_typology",
            "Dec_Lat",
            "Dec_Long"]

SHEET2 = "CorkHarbour_2010_2018"
# 27 desired columns
COLUMNS2 = ["Sample_ID",
            "Station_No",
            "Sample_Label",
            "Date",
            "Time",
            "Depth_Bed",
            "Depth_Sample",
            "Salinity",
            "Temperature",
            "pH",
            "Secchi",
            "DO_saturation",
            "DO_mgL",
            "BOD",
            "TON",
            "NH3",
            "PO4",
            "chl_a",
            "SiO2",
            "SS",
            "Colour",
            "DIN",
            "Free_NH3",
            "\"TON:NH3\"",
            "\"DIN:PO4\"",
            "\"DIN:Si\"",
            "\"P:Si\""]

BASIC = ["Sample_ID",
         "Station_No",
         "Sample_Label",
         "Date",
         "Time",
         "Year",
         "WB_Name",
         "Station_No",
         "Location",
         "WB_typology",
         "Dec_Lat",
         "Dec_Long"]

POLLUTANTS = ["Depth_Bed",
              "Depth_Sample",
              "Salinity",
              "Temperature",
              "pH",
              "Secchi",
              "DO_saturation",
              "DO_mgL",
              "BOD",
              "TON",
              "NH3",
              "PO4",
              "chl_a",
              "SiO2",
              "SS",
              "Colour",
              "DIN",
              "Free_NH3",
              "\"TON:NH3\"",
              "\"DIN:PO4\"",
              "\"DIN:Si\"",
              "\"P:Si\""]

UNITS = {
    "Depth_Bed": "m",
    "Depth_Sample": "m",
    "Salinity": "%",
    "Temperature": "°C",
    "pH": None,
    "Secchi": "m",
    "DO_saturation": "%sat",
    "DO_mgL": "mg/l",
    "BOD": "mg/l",
    "TON": "mg/l",
    "NH3": "mg/l",
    "PO4": "µg/l",
    "chl_a": "mg/m3",
    "SiO2": "µg/l",
    "SS": "mg/l",
    "Colour": None,
    "DIN": "mg/l",
    "Free_NH3": None,
    "\"TON:NH3\"": "molar ratio",
    "\"DIN:PO4\"": "molar ratio",
    "\"DIN:Si\"": "molar ratio",
    "\"P:Si\"": "molar ratio"
}

PARAMETER_FULLNAME = {
    "Depth_Bed": "Depth of seabed (m)",
    "Depth_Sample": "Depth of sample (m)",
    "Salinity": "Salinity (%)",
    "Temperature": "Temperature (°C)",
    "pH": "pH",
    "Secchi": "Secchi depth (m)",
    "DO_saturation": "Dissolved Oxygen saturation(%sat)",
    "DO_mgL": "Dissolved Oxygen (mg/l)",
    "BOD": "BOD (mg/l)",
    "TON": "TON (mg/l)",
    "NH3": "NH3 (mg/l)",
    "PO4": "PO4 (µg/l)",
    "chl_a": "Chlorophyll  (mg/m3)",
    "SiO2": "SiO2 (µg/l)",
    "SS": "Suspended solids (mg/l)",
    "Colour": "Colour",
    "DIN": "DIN (mg/l)",
    "Free_NH3": "Free NH3",
    "\"TON:NH3\"": "\"TON:NH3\" (molar ratio)",
    "\"DIN:PO4\"": "\"DIN:PO4\" (molar ratio)",
    "\"DIN:Si\"": "\"DIN:Si\" (molar ratio)",
    "\"P:Si\"": "\"P:Si\" (molar ratio)"
}

