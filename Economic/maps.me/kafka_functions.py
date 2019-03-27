"""
Written by Karypidis Paris Alexandros
Democritus University of Thrace (DUTH)
2018 within CUTLER H2020 Project
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


