import pandas as pd
from nltk.stem import *
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

def pre_process(text):
    """
    Pre processes a given document by removing apostrophes, tokenizing, which includes the removal of punctuation,
    lowercasing and stemming with the PorterStemmer.

    :param text: The text, which is to be pre processed.
    :return:     The pre processed text in the form a whitespace delimited String containing the processed words in the
                 original order.
    """
    text = remove_stop_words(
            to_lower(
                tokenize(
                    replace_apostrophe(text)
                    )
                )
            )
    return ' '.join(text)


def stem(tokens):
    """
    Stems the given token with the nltk.stem.PorterStemmer.

    :param tokens: The words, which should be stemmed.
    :return:       A List containing the stemmed words.
    """
    stemmer = PorterStemmer()
    return [stemmer.stem(token) for token in tokens]


def tokenize(text):
    """
    Tokenizes the text and removes punctuation.

    :param text: The text, which should be tokenized
    :return:     The tokenized text.
    """
    tokenizer = RegexpTokenizer(r'\w+')
    return tokenizer.tokenize(text)


def replace_apostrophe(text):
    """
    Removes apostrophes from the given text.

    :param text: The text, for which apostrophes should be removed.
    :return:     The original text with removed apostrophes, eg. isn't results in isnt.
    """
    text = text.replace('/', '')
    return text.replace('\'', '')


def to_lower(text):
    """
    Returns a list of the lowercased words.

    :param text: The text to be put in lower case.
    :return:      a list of the lowercased words.
    """
    return [token.lower() for token in text]


def remove_stop_words(text):
    stop_words = set(stopwords.words('english'))
    stop_words.add('well')

    text = [token for token in text if not token in stop_words]

    # remove short words
    return [token for token in text if len(token) >= 3 ]

def remove_stop_words_summarization(text):
    stop_words = set(stopwords.words('english'))
    stop_words.add('well')

    text = [token for token in text if not token in stop_words]

    # remove short words
    return [token for token in text]
