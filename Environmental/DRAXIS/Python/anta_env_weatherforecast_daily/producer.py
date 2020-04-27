"""
This code is open-sourced software licensed under the MIT license. (http://opensource.org/licenses/MIT)

Copyright 2020 Stergios Bampakis, DRAXIS ENVIRONMENTAL S.A.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

DISCLAIMER

This code is used to crawl/parse data from Weather Forecast - DRAXIS API (https://api.draxis.gr/).
By downloading this code, you agree to contact the corresponding data provider
and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process)
all data obtained from the data source.

"""

import os
import json
import requests
from kafka import KafkaProducer
from dotenv import load_dotenv
from constants import *


def get_seven_day_forecast():
    """
    Method that issues request to DRAXIS API for the seven day forecast.
    Check for more info: https://api.draxis.gr/#weather-hourly-data

    Returns:
        dict: The response data of the forecast.

    """

    params = {
        "lat": ANTA_LAT,
        "lon": ANTA_LON,
        "resolution": ANTA_RESOLUTION,
        "from_date": FROM_DATE,
        "to_date": TO_DATE,
        "variables": ','.join(VARIABLES),
        # "timezone": TIMEZONE,
        "apikey": os.getenv("API_KEY")
    }

    url = os.getenv("DRAXIS_API_WEATHER_FORECAST_URL")
    response = requests.get(url=url, params=params)

    return response.json()


# Load environment variables
load_dotenv()

producer = KafkaProducer(bootstrap_servers=["{}:{}".format(os.getenv('KAFKA_HOST'), os.getenv('KAFKA_PORT'))],
                         security_protocol=os.getenv('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT'),
                         ssl_cafile=os.getenv('KAFKA_CA_FILE', None),
                         ssl_certfile=os.getenv('KAFKA_CERT_FILE', None),
                         ssl_keyfile=os.getenv('KAFKA_KEY_FILE', None),
                         value_serializer=lambda m: json.dumps(m).encode('utf8'))


# Get the seven days forecast
forecast = get_seven_day_forecast()
print(forecast)
producer.send(KAFKA_TOPIC, forecast)

# Make the assumption that all messages are published and consumed
producer.send(KAFKA_TOPIC_FINISH, 'All messages are published and consumed successfully!')

producer.flush()
