##This code is open-sourced software licensed under the MIT license
##Copyright 2019 Karypidis Paris - Alexandros, Democritus University of Thrace (DUTH)
##Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
##The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
##THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
##
##DISCLAIMER
##This code is used to crawl/parse data from Eurostat databases. By downloading this code, you agree to contact the corresponding data provider and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process) all data obtained from the data source.

"""
CUTLER H2020 Project
Python 3.5

connect_kafkaproducer - Function
    Connects to KAFKA

publish_message - Function
    Publishes message into a KAFKA topic

kafkasendmessage - Function
    Uses the previous functions to send messages into KAFKA - Use this in crawler python file
"""

from kafka import KafkaConsumer, KafkaProducer

DEBUG = True

def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10))
    except Exception as ex:
        if DEBUG:
            print('[-] Exception while connecting KAFKA')
        print(str(ex))
    finally:
        return _producer

def publish_message(producer_instance, topic_name, key, value):
    try:
        key_bytes = bytes(key, encoding='utf-8')
        value_bytes = bytes(value, encoding='utf-8')
        producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
        producer_instance.flush()
        if DEBUG:
            print('[+] Message to KAFKA published successfully.')
    except Exception as ex:
        if DEBUG:
            print('[-] Exception in publishing message to KAFKA')
        print(str(ex))


def kafkasendmessage(topic, message):

    if DEBUG:
        print("[+] Ingesting to KAFKA... message: " + message + " into topic: " + topic)
    kafka_producer = connect_kafka_producer()
    publish_message(kafka_producer, topic, 'raw', message)
    if kafka_producer is not None:
        kafka_producer.close()


