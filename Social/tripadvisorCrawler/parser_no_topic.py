#!/usr/bin/env python3
# ./parser4nico.py filename
import sys
import re
import numpy as np
import pandas as pd
import os

from nltk.sentiment.vader import SentimentIntensityAnalyzer

from get_corpus import *
from get_metadata import *
from hmdp import *
from topic_labeling import *
from pre_process_funcs import *

filename = sys.argv[1]
#point_of_interest = sys.argv[2]

# read data
df = pd.read_csv(filename, parse_dates=[5], header=None)
df.columns = [ 'comment_title', 'user_id', 'rating', 'num_helpful','comment', 'date_of_experience' ]

# sentiment analysis
sid = SentimentIntensityAnalyzer()
df['sentiment'] = df['comment'].apply(lambda x: sid.polarity_scores(x)['compound'])

# clean data
df = df[df.date_of_experience.notna()].reset_index(drop=True)


# summarization
from filter_trigram import *
import spacy, nltk
import pytextrank

nlp = spacy.load('en_core_web_sm')
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

