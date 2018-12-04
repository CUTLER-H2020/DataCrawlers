"""
contains mappings between the four targeted cities in CUTLER, their first order administrative division (ADM1)
as is used in the GDELT project and their geolocation in latitude and longitude.
See https://blog.gdeltproject.org/gdelt-geo-2-0-api-debuts/
and http://data.gdeltproject.org/api/v2/guides/LOOKUP-ADM1S.TXT
for further information on ADM1 and how it is used to query the GDELT data.
"""

cities = {
    "Antalya": {
        "adm1": "TU07",
        "lat": 36.9,
        "long": 30.68333,
    },
    "Antwerp": {
        "adm1":  "BE01",
        "lat": 51.260197,
        "long": 4.402771,
    },
    "Cork": {
        "adm1": "EI04",
        "lat": 51.903614,
        "long": -8.468399,
    },
    "Thessaloniki": {
        "adm1": "GR59",
        "lat": 	40.736851,
        "long": 22.920227,
    },
}
