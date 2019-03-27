"""
Written by Karypidis Paris Alexandros
Democritus University of Thrace (DUTH)
2018 within CUTLER H2020 Project
Python 3.5

connect_elasticsearch - Function
    Connects to elasticsearch

send_to_elasticsearch - Function
    Ingests data to elasticsearch - Use this in crawler python file
"""

from datetime import datetime
from elasticsearch import Elasticsearch

DEBUG = True

def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if DEBUG:
        if _es.ping():
            print('[+] Connected to elasticsearch successfully')
        else:
            print('[-] Couldn\'t connect to elasticsearch')
    return _es

def send_to_elasticsearch(index_name, data, doc_type):

    es = connect_elasticsearch()
    res = es.index(index=index_name, doc_type=doc_type, body=data)
#    print(res['result'])

