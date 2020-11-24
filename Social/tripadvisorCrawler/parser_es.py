#!/usr/bin/env python3
# ./parser_es.py filename point_of_interest
import sys
import re
import numpy as np
import pandas as pd
import os

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# Elasticsearch connection
es_url = 'http://141.26.209.12:9200'
es = Elasticsearch(es_url)

filename = sys.argv[1]
point_of_interest = sys.argv[2]

# read data
df = pd.read_csv(filename, parse_dates=[5])
#df.columns = [ 'comment_title', 'user_id', 'rating', 'num_helpful','comment', 'date_of_experience', 'sentiment', 'topic_id', 'topic' ]

df['point_of_interest'] = point_of_interest

# prepare data
doc = {}
doc = df.to_dict(orient='record')

# push data to es
bulk(es, doc, index='cutler_tripadvisor', doc_type='_doc', raise_on_error=True)
