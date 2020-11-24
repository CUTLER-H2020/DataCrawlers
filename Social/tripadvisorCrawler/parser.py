#!/usr/bin/env python3
# ./parser.py filename point_of_interest server
import sys
import re
import numpy as np
import pandas as pd

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from get_corpus import *
from get_metadata import *
from hmdp import *
from topic_labeling import *

filename = sys.argv[1]
point_of_interest = sys.argv[2]
server = sys.argv[3]

# Elasticsearch connection
if server == 'dell':
    es_url = 'http://10.10.2.56:9200'
elif server == 'uniko':
    es_url = 'http://141.26.209.12:9200'

es = Elasticsearch(es_url)

# read data
df = pd.read_json(filename, convert_dates=[2])
df.columns = [ 'comment_title', 'comment', 'date_of_experience' ]

# sentiment analysis
sid = SentimentIntensityAnalyzer()
df['sentiment'] = df['comment'].apply(lambda x: sid.polarity_scores(x)['compound'])

df['point_of_interest'] = point_of_interest

# topic modelling
df = get_and_write_corpus(df)
df = get_and_write_metadata(df)
hmdp = HMDP(MIN_DICT_WORDS=5, RUNS=200, T=8)
hmdp.run()
df = hmdp.get_comment_topics(df)
#mmr = MMR()
#df = mmr.get_ranking(df, 0.8)
df = trigram_labels(df, hmdp)
df = df.drop(columns=['processed'])

# clean data
df = df[df.date_of_experience.notna()]

# prepare data
doc = {}
doc = df.to_dict(orient='record')

# push data to es
bulk(es, doc, index='cutler_tripadvisor', doc_type='_doc', raise_on_error=True)
