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

This code is used to crawl/parse data from Thessaloniki's traffic report website (https://www.trafficthessreports.imet.gr/)
By downloading this code, you agree to contact the corresponding data provider
and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process)
all data obtained from the data source.

"""

import os
import json
from urllib.parse import quote, urljoin

import requests
import pandas as pd
import datetime

from kafka import KafkaProducer
from dotenv import load_dotenv
from bs4 import BeautifulSoup

from constants import *


def __get_viewstate_from_html(html):
    """
    Method to get the __VIEWSTATE value from an html page

    """

    soup = BeautifulSoup(html, features='html.parser')

    # Find the input hidden field with name __VIEWSTATE and get it's value
    input_viewstate = soup.find(attrs={"name": "__VIEWSTATE"})

    return input_viewstate['value']


def get_viewstate_after_login():
    """
    Method that executes login to the website and returns the required __VIEWSTATE
    for the POST request to get the csv with the data

    """

    url = LOGIN_URL

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    def _get_initial_viewstate():
        _res = requests.post(url=url)
        return __get_viewstate_from_html(_res.text)

    data = {
        "__VIEWSTATE": _get_initial_viewstate(),
        # "__VIEWSTATEGENERATOR": "E8287760",
        "Login1$UserName": os.getenv('TRAFFIC_IMET_EMAIL'),
        "Login1$Password": os.getenv('TRAFFIC_IMET_PASSWORD'),
        "Login1$LoginButton": "Είσοδος"
    }

    res = requests.post(url=url, headers=headers, data=data)

    return __get_viewstate_from_html(res.text)


def get_data_url(route_id: int, from_date: str, from_time: str, to_date: str, to_time: str):
    url = urljoin(BASE_URL, "/export.aspx")

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        "ExportDropDownList": "_speed{}".format(route_id),
        "FromDateHiddenField": from_date,
        "FromTimeHiddenField": from_time,
        "ToDateHiddenField": to_date,
        "ToTimeHiddenField": to_time,
        "__VIEWSTATE": get_viewstate_after_login(),
        # "__VIEWSTATEGENERATOR": "E8287760",
        "ExportButton": "Εξαγωγή"
    }

    res = requests.post(url=url, headers=headers, data=data)

    html = res.text
    soup = BeautifulSoup(html, features='html.parser')

    all_links = soup.find_all('a')
    for a in all_links:
        if a['href'].startswith("Files"):
            # found the link of the csv
            # return it encoded with BASE_URL as prefix in order
            # pandas to load it as a DataFrame
            csv_link = a['href']
            csv_link = quote(csv_link)
            csv_link = urljoin(BASE_URL, csv_link)

            print("Full path csv link: {}".format(csv_link))
            return csv_link
    raise ThessImetException("No csv link found. Please check your parameters.\n 1. from_date <= to_day \n 2. "
                             "should be in the following format: \n - from_date/to_date: dd-mm-yyyy \n - "
                             "from_time/to_time: HH:mm. \n You gave dates: {}, {} \n and times: {}, {}"
                             .format(from_date, to_date, from_time, to_time))


def broadcast_data(route_name: str, csv: str, producer=None):
    df = pd.read_csv(csv)
    # these apply to all records
    mileage = 100
    mileage_unit = "vkm (km*cars)"

    # make Timestamp column type datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # drop column Name that contains greek chars.
    # we will replace it with our greeklish mapping
    df.drop(columns=['Name'], inplace=True)

    payload = {
        'mileage': mileage,
        'mileage_unit': mileage_unit,
        'unit': "u (km/h)",
        'name': route_name
    }

    for index, row in df.iterrows():
        data = row.to_dict()

        # populate the payload based on the previous index's field names
        payload['id'] = data['PathID']

        # this is the format of date at the previous (same) index
        payload['date'] = data['Timestamp'].strftime('%Y/%m/%d %H:%M:%S')

        payload['samples'] = data['Samples']
        payload['speed'] = data['Value']

        print(payload)
        producer.send(KAFKA_TOPIC, payload)

    print(df)


if __name__ == '__main__':
    load_dotenv()

    producer = KafkaProducer(bootstrap_servers=["{}:{}".format(os.getenv('KAFKA_HOST'), os.getenv('KAFKA_PORT'))],
                             security_protocol=os.getenv('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT'),
                             ssl_cafile=os.getenv('KAFKA_CA_FILE', None),
                             ssl_certfile=os.getenv('KAFKA_CERT_FILE', None),
                             ssl_keyfile=os.getenv('KAFKA_KEY_FILE', None),
                             value_serializer=lambda m: json.dumps(m).encode('utf8'))

    today_obj = datetime.datetime.today()
    yesterday_obj = today_obj - datetime.timedelta(days=1)

    date_today = today_obj.strftime('%d-%m-%Y')
    time_today = today_obj.strftime('%H:%M')

    date_yesterday = yesterday_obj.strftime('%d-%m-%Y')
    time_yesterday = yesterday_obj.strftime('%H:%M')

    for route, route_id in ROUTE_IDS.items():
        csv = get_data_url(route_id=route_id,
                           from_date=date_yesterday,
                           from_time=time_yesterday,
                           to_date=date_today,
                           to_time=time_today)

        broadcast_data(route, csv, producer)

    # Make the assumption that all messages are published and consumed
    producer.send(KAFKA_TOPIC_FINISH, 'All messages are published and consumed successfully!')
    producer.flush()
