import nltk
import numpy as np
import pandas as pd

from pre_process_funcs import *

"""
Contains functions to label topic clusters using either topic word distribution or the most frequent words in comments.
For both cases bigrams and trigrams can be extracted as labels.
"""


def get_words(comments):
    """
    Returns a list of all words in the lowercased comments with stop words and punctuation removed.

    :param comments: pandas.DataFrame The comments with a column "text" containing the raw comment text.
    :return:
    """
    return " ".join(comments.processed.map(lambda text: " ".join(
        remove_stop_words(
            to_lower(
                tokenize(
                    replace_apostrophe(text)
                )
            )
        )
    )).tolist()).split(" ")


def bigram_labels(comments, hmdp):
    """
    Finds the bigram with the largest sum of size of intersection between label and top words under topic-word
    distribution and probability of label words under topic-word distribution.

    :param hmdp:     HMDP
    :param comments: pandas.DataFrame The comments with a column indicating topic by topic_id.

    :return:         pandas.DataFrame The labeled comments.
    """
    filter_ = lambda word1, word2: len({word1, word2}.intersection(set(words.split(" ")))) == 0

    for topic in comments["topic_id"]:

        words = comments[comments["topic_id"] == topic]["topic"].iloc[0]
        twdist = hmdp.get_topic_word_dist(topic)

        # find bigrams from comments
        tokenizer = RegexpTokenizer(r'\w+')
        bigrams = nltk.collocations.BigramCollocationFinder.from_words(
            #get_words(clusters[topic]["comments"])
            " ".join(comments[comments["topic_ id" == topic]].text.apply(lambda text: " ".join(tokenizer.tokenize(text)))
                     .str.lower().tolist()).split(" ")
        )

        # filtering of bigrams with no intersection with the top K words of the topic
        bigrams.apply_ngram_filter(filter_)
        bigram_measures = nltk.collocations.BigramAssocMeasures()
        # filtering of infrequent bigrams for performance
        top = bigrams.nbest(bigram_measures.raw_freq , 15000)

        if len(top) > 0:
            stemmer = PorterStemmer()
            score = lambda tpl: len(set(tpl).intersection(set(words.split(" ")))) + np.sum(
                [twdist[stemmer.stem(word)] if stemmer.stem(word) in twdist else 0 for word in tpl]
            )
            scores = pd.DataFrame(columns=["bigram", "score"])

            for i, tpl in enumerate(top):
                scores.at[i, "bigram"] = tpl
                scores.at[i, "score"] = score(tpl)

            labels = scores[scores.score == scores.score.max()]
            comments.loc[comments["topic_id"] == topic, "topic"] = " ".join(
                (labels.sample(1) if len(labels) > 1 else labels)["bigram"].iloc[0])

    return comments


def trigram_labels(comments, hmdp):
    """
    Finds the trigram with the largest sum of size of intersection between label and top words under topic-word
    distribution and probability of label words under topic-word distribution.

    :param hmdp:     HMDP
    :param comments: pandas.DataFrame The comments with columns keys indicating topic by topic_id.

    :return:         pandas.DataFrame The labeled comments.
    """
    filter_ = lambda word1, word2, word3: len({word1, word2, word3}.intersection(set(words.split(" ")))) == 0

    for topic in comments["topic_id"]:

        words = comments[comments["topic_id"] == topic]["topic"].iloc[0]
        twdist = hmdp.get_topic_word_dist(topic)

        # find trigrams from comments
        tokenizer = RegexpTokenizer(r'\w+')
        trigrams = nltk.collocations.TrigramCollocationFinder.from_words(
            #get_words(clusters[topic]["comments"])
            " ".join(comments[comments["topic_id"] == topic].processed.apply(lambda text: " ".join(
                tokenizer.tokenize(text))).str.lower().tolist()).split(" ")
        )

        # filtering of trigrams with no intersection with the top K words of the topic
        trigrams.apply_ngram_filter(filter_)
        trigram_measures = nltk.collocations.TrigramAssocMeasures()
        # filtering of infrequent trigrams for performance
        top = trigrams.nbest(trigram_measures.raw_freq , 15000)

        if len(top) > 0:
            stemmer = PorterStemmer()
            score = lambda tpl: len(set(tpl).intersection(set(words.split(" ")))) + np.sum(
                [
                    twdist[stemmer.stem(word)]
                    if stemmer.stem(word) in twdist
                    else 0
                    for word in tpl
                ]
            )
            scores = pd.DataFrame(columns=["trigram", "score"])

            for i, tpl in enumerate(top):
                scores.at[i, "trigram"] = tpl
                scores.at[i, "score"] = score(tpl)

            labels = scores[scores.score == scores.score.max()]
            comments.loc[comments["topic_id"] == topic, "topic"] = " ".join(
                (labels.sample(1) if len(labels) > 1 else labels)["trigram"].iloc[0])
            print(comments.loc[comments["topic_id"] == topic, "topic"])

    return comments
