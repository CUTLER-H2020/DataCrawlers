import os
import json
import pandas as pd
import datetime
from kafka import KafkaProducer
from dotenv import load_dotenv
from constants import *


def parse_excel(excel):
    df = pd.read_excel(EXCEL_FILE, skiprows=[1], usecols=[0, 1, 2, 8, 10, 11, 12, 15])

    # The structure of the raw data (distribution of data per rows) is ready to be broadcasted by Kafka
    # Also the desired data types are (almost) ready with the magic of Pandas except time
    # which we need to convert to str, in order to be JSON serializable for Kafka

    # Replace nan values with None
    # to avoid errors later in ES mapping.
    df = df.where(pd.notnull(df), None)

    sent_messages = 0
    for index, row in df.iterrows():
        data = row.to_dict()
        datetime_obj = data.pop('Date')

        # convert from datetime object to time string with iso format, example: '2008-03-05T12:00:00'
        date = datetime_obj.isoformat()

        year_str = datetime_obj.year.__str__()  # Add year field for Kibana-reasons

        data['date'] = date
        # Save year as int instead of str, in order DRAXIS gauge plugin to work.
        # check: https://jira.draxis.gr/browse/CUTL-109
        data['year'] = int(year_str)
        print(data)
        producer.send(KAFKA_TOPIC, data)
        sent_messages += 1

    print("Broadcasted total messages: {}".format(sent_messages))


load_dotenv()

producer = KafkaProducer(bootstrap_servers=["{}:{}".format(os.getenv('KAFKA_HOST'), os.getenv('KAFKA_PORT'))],
                         security_protocol=os.getenv('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT'),
                         ssl_cafile=os.getenv('KAFKA_CA_FILE', None),
                         ssl_certfile=os.getenv('KAFKA_CERT_FILE', None),
                         ssl_keyfile=os.getenv('KAFKA_KEY_FILE', None),
                         value_serializer=lambda m: json.dumps(m).encode('utf8'))

parse_excel(EXCEL_FILE)

# Make the assumption that all messages are published and consumed
producer.send(KAFKA_TOPIC_FINISH, 'All messages are published and consumed successfully!')
producer.flush()
