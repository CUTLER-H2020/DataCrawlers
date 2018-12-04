import nltk
import numpy as np
from sklearn.externals import joblib


class CommentClassifier:

    stop_words = np.array(['share', 'shares', 'like', 'report', 'sign', 'register', 'comment', 'facebook',
                           'twitter', 'tumblr', 'reddit', 'login', 'reply', 'replies', 'flag', 'minutes', 'minute'
                           'hours', 'hour', 'ago', 'days', 'day', 'months', 'month' 'likes', 'sort', 'newest', 'oldest',
                           'follow', 'view', 'comments', 'recommendations', 'leave', 'post', 'create', 'account',
                           'username', 'a', 'sign-up', 'signup'])

    def __init__(self, clf_path, word_features_path):
        self.clf = joblib.load(clf_path)
        self.word_features = joblib.load(word_features_path)

    def get_features(self, document, word_features):
        """
        Returns the feature matrix for the classifier consisting of the prevalence of the most frequent worrds
        and the lenght of the comment
        :param document: The comment to be classified
        :param word_features: the most frequent words
        :return: the feature matrix
        """
        document_words = set(document)
        features = [(word in document_words) for word in word_features]
        # number of words in document
        features.append(len(document))
        return features

    def pre_process(self, comment):
        """
        Preprocesses the given comment by tokenizing, removing punctuation and removing stop words
        :param comment: the comment to pre-process
        :return: the pre-processed comment
        """
        comment = comment.strip()
        tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
        tokenized_c = tokenizer.tokenize(comment)
        filtered_c = [w for w in tokenized_c if not w.lower() in self.stop_words]
        return filtered_c