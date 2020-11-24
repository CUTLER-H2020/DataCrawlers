#!/usr/bin/env python3
# ./parser4nico.py filename
import sys
import re
import numpy as np
import pandas as pd
import os
import dateparser

from nltk.sentiment.vader import SentimentIntensityAnalyzer

from get_corpus import *
from get_metadata import *
from hmdp import *
from topic_labeling import *
from pre_process_funcs import *

filename = sys.argv[1]
#point_of_interest = sys.argv[2]

# read data
df = pd.read_csv(filename, header=None)
df.columns = [ 'comment_title', 'user_id', 'rating', 'num_helpful','comment', 'date_of_experience' ]

# fix Italian dates
df['date_of_experience'] = df['date_of_experience'].astype(str).apply(lambda x: dateparser.parse(x, date_formats=[': %B %Y'], settings={'PREFER_DAY_OF_MONTH': 'first'}))

# sentiment analysis - not implemented for Italian
df['sentiment'] = 0

# clean data
df = df[df.date_of_experience.notna()].reset_index(drop=True)

# topic modelling
#topic_numbers = int(np.log(len(df))*1.6)
df = get_and_write_corpus(df)
df = get_and_write_metadata(df)
hmdp = HMDP(MIN_DICT_WORDS=5, RUNS=100, T=8)
hmdp.run()
df = hmdp.get_comment_topics(df)
#mmr = MMR()
#df = mmr.get_ranking(df, 0.8)

# topic labelling
from filter_trigram import *

# get and save trigram topic labels
#df = hmdp.get_trigram_labels(df, filename + '.topic_labels')
#df = df.drop(columns=['processed'])

#for t in set(df['topic_id']):
#    trigram = df[df['topic_id'] == t]['topic'].values[0]
#
#    print('raw: ', trigram)
#    sentences = df[df['topic_id'] == t]['comment']
#    # examine the top-ranked phrases in the document
#    #for p in doc._.phrases:
#    # ...:     print('{:.4f} {:5d}  {}'.format(p.rank, p.count, p.text))
#    # ...:     print(p.chunks)
#
#    #topic_label = get_trigram(text, trigram)
#    df.loc[df['topic_id'] == t, 'topic'] = topic_label

# summarization
import spacy, nltk
import pytextrank

nlp = spacy.load('it_core_news_sm')
tr = pytextrank.TextRank()
nlp.add_pipe(tr.PipelineComponent, name='textrank', last=True)

def summarize(comment, nlp):
    sentences = comment.replace(',', '.')
    sentences = sentences.replace(':', '.')
    sentences = nltk.sent_tokenize(sentences)

    sentences = [ ' '.join(
        #remove_stop_words_summarization(
        to_lower(tokenize(replace_apostrophe(s)))) for s in sentences ]
    text = '. '.join(sentences)

    doc = nlp(text)

    terms = [ p.text for p in doc._.phrases if (p.rank > .1) & (len(p.text.split(' ')) > 1) ]

    terms = [ [term] if len(term.split(' ')) < 3 else extract_terms(term) for term in terms ]
    #terms = [ extract_terms(term) for term in terms ]
    #print(terms)

    # flatten the list of terms
    #https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists?page=1&tab=votes#tab-top
    terms = [ item for sublist in terms for item in sublist ]

    return terms

df['summarization'] = df['comment'].apply(lambda x: summarize(x, nlp))

# anonymization
df['user_id'] = 'Anonymized User'

df.to_csv(filename + '.csv', line_terminator='\r\n')

