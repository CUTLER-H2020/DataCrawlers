import csv, os, shutil
import subprocess

import nltk
import pandas as pd
import numpy as np

from nltk.stem import *
from nltk.tokenize import RegexpTokenizer

class HMDP:
    """
    This wrapper around the Promoss HMDP implementation (https://github.com/ckling/promoss) takes inspiration from the
    notebook https://github.com/ckling/promoss/blob/master/ipynb/hmdp.ipynb published with the promoss package and
    modifies it to the needs of this thesis as is granted under the terms of the GNU General Public License as published
    by the Free Software Foundation.

    It contains the necessary functions to run the model and connect the documents with their assigned topics.
    """

    def __init__(self,
                 directory=None,
                 meta_params=None,
                 RUNS=None,
                 T=None,
                 SAVE_STEP=10,
                 TRAINING_SHARE=1,
                 BATCHSIZE=128,
                 BATCHSIZE_GROUPS=128,
                 BURNIN=0,
                 BURNIN_DOCUMENTS=0,
                 INIT_RAND=0,
                 SAMPLE_ALPHA=1,
                 BATCHSIZE_ALPHA=1000,
                 MIN_DICT_WORDS=1,
                 alpha_0=1,
                 alpha_1=1,
                 epsilon="none",
                 delta_fix="none",
                 rhokappa=0.5,
                 rhotau=64,
                 rhos=1,
                 rhokappa_document=0.5,
                 rhotau_document=64,
                 rhos_document=1,
                 rhokappa_group=0.5,
                 rhotau_group=64,
                 rhos_group=1,
                 processed=True,
                 stemming=False,
                 stopwords=False,
                 language="en",
                 store_empty=True,
                 topk=15,
                 gamma=1,
                 learn_gamma=True
                 ):
        """

        :param meta_params: The value needed for the meta_params flag of the implementation as specified in
                            https://github.com/ckling/promoss.
        """
        if directory is None:
            directory = os.path.join(os.getcwd(), '')
        self.directory = directory

        if meta_params is None:
            meta_params = "N"
        self.meta_params = meta_params

        if RUNS is None:
            RUNS = 100
        self.RUNS = RUNS

        if T is None:
            T = 100
            #T = self.estimate_t()
        self.T = T

        if TRAINING_SHARE is None:
            TRAINING_SHARE = 1
        self.TRAINING_SHARE = TRAINING_SHARE

        self.SAVE_STEP = SAVE_STEP
        self.TRAINING_SHARE = TRAINING_SHARE
        self.BATCHSIZE = BATCHSIZE
        self.BATCHSIZE_GROUPS = BATCHSIZE_GROUPS
        self.BURNIN = BURNIN
        self.BURNIN_DOCUMENTS = BURNIN_DOCUMENTS
        self.INIT_RAND = INIT_RAND
        self.SAMPLE_ALPHA = SAMPLE_ALPHA
        self.BATCHSIZE_ALPHA = BATCHSIZE_ALPHA
        self.MIN_DICT_WORDS = MIN_DICT_WORDS
        self.alpha_0 = alpha_0
        self.alpha_1 = alpha_1
        self.epsilon = epsilon
        self.delta_fix = delta_fix
        self.rhokappa = rhokappa
        self.rhotau = rhotau
        self.rhos = rhos
        self.rhokappa_document = rhokappa_document
        self.rhotau_document = rhotau_document
        self.rhos_document = rhos_document
        self.rhokappa_group = rhokappa_group
        self.rhotau_group = rhotau_group
        self.rhos_group = rhos_group
        self.processed = processed
        self.stemming = stemming
        self.stopwords = stopwords
        self.language = language
        self.store_empty = store_empty
        self.topk = topk
        self.gamma = gamma
        self.learn_gamma = learn_gamma

    def run(self):
        """
        Runs the HMDP model. See https://github.com/ckling/promoss.

        :return:
        """

        print("Running HMDP topic model... (please wait)")

        if os.path.isdir(self.directory + "/output_HMDP"):
            shutil.rmtree(self.directory + "/output_HMDP")
        if os.path.isdir(self.directory + "/cluster_desc"):
            shutil.rmtree(self.directory + "/cluster_desc")

        if os.path.isfile(self.directory + "/groups"):
            os.remove(self.directory + "/groups")
        if os.path.isfile(self.directory + "/groups.txt"):
            os.remove(self.directory + "/groups.txt")
        if os.path.isfile(self.directory + "/text.txt"):
            os.remove(self.directory + "/text.txt")
        if os.path.isfile(self.directory + "/words.txt"):
            os.remove(self.directory + "/words.txt")
        if os.path.isfile(self.directory + "/wordsets"):
            os.remove(self.directory + "/wordsets")

        if not os.path.isfile("../../lib/promoss.jar"):
            print("Could not find ../../lib/promoss.jar. Exit")
            return
        try:
            with subprocess.Popen(['java', '-jar', '../../lib/promoss.jar',
                                   '-directory', self.directory,
                                   '-meta_params', self.meta_params,
                                   '-T', str(self.T),
                                   '-RUNS', str(self.RUNS),
                                   '-SAVE_STEP', str(self.SAVE_STEP),
                                   '-TRAINING_SHARE', str(self.TRAINING_SHARE),
                                   '-BATCHSIZE', str(self.BATCHSIZE),
                                   '-BATCHSIZE_GROUPS', str(self.BATCHSIZE_GROUPS),
                                   '-BURNIN', str(self.BURNIN),
                                   '-BURNIN_DOCUMENTS', str(self.BURNIN_DOCUMENTS),
                                   '-INIT_RAND', str(self.INIT_RAND),
                                   '-SAMPLE_ALPHA', str(self.SAMPLE_ALPHA),
                                   '-BATCHSIZE_ALPHA', str(self.BATCHSIZE_ALPHA),
                                   '-MIN_DICT_WORDS', str(self.MIN_DICT_WORDS),
                                   '-alpha_0', str(self.alpha_0),
                                   '-alpha_1', str(self.alpha_1),
                                   '-epsilon', str(self.epsilon),
                                   '-delta_fix', str(self.delta_fix),
                                   '-rhokappa', str(self.rhokappa),
                                   '-rhotau', str(self.rhotau),
                                   '-rhos', str(self.rhos),
                                   '-rhokappa_document', str(self.rhokappa_document),
                                   '-rhotau_document', str(self.rhotau_document),
                                   '-rhos_document', str(self.rhos_document),
                                   '-rhokappa_group', str(self.rhokappa_group),
                                   '-rhotau_group', str(self.rhotau_group),
                                   '-rhos_group', str(self.rhos_group),
                                   '-processed', str(self.processed),
                                   '-stemming', str(self.stemming),
                                   '-stopwords', str(self.stopwords),
                                   '-language', str(self.language),
                                   '-store_empty', str(self.store_empty),
                                   '-topk', str(self.topk),
                                   '-gamma', str(self.gamma),
                                   '-learn_gamma', str(self.learn_gamma)
                                   ], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:

                for line in p.stdout:
                    line = str(line)[2:-1].replace("\\n", "").replace("\\t", "   ")
                    print(line, end='\n')
                for line in p.stderr:
                    line = str(line)[2:-1].replace("\\n", "").replace("\\t", "   ")
                    print(line, end='\n')

        except subprocess.CalledProcessError as e:
            print(e.returncode)
            print(e.output)

    def get_topics(self):
        """
        Returns a pandas.DataFrame with the topics and a dictionary mapping each topics k top words to their
        probability.

        TODO: implement dictionary

        :return:
        """
        return pd.read_csv('output_HMDP/{}/topktopic_words'.format(self.RUNS), delimiter='\t', header=None, names=['topkwords'])

    def get_doc_topic_dist(self):
        """
        Returns the document-topic distribution for each of the documents in the corpus.

        :return: pandas.DataFrame Containing the document-topic distribution for each of the documents in the corpus.
                                  Each column represents one topic. The row sorting matches that of the corpus.txt
                                  and meta.txt and the column sorting that of the topktopics file created by the HMDP
                                  implementation.
        """
        return pd.read_csv('output_HMDP/{}/doc_topic'.format(self.RUNS), header=None)

    def get_comment_topics(self, comments):
        """
        Returns the pandas.DataFrame of the comments with an additional column containing a topic identifier.

        :return: pandas.DataFrame Of the comments with an additional column containing a topic identifier.
                                  The identifier specifies the column in the pandas.DataFrame created by
                                  self.get_doc_topic_dist().
        """
        # only the last k distributions are needed as the first n-k distributions model the document-topic distribution
        # of the articles (disabled due to reindexing)
        doc_topic_dist = self.get_doc_topic_dist()
        # the column index with the highest value represents the most likely topic
        comments['topic_id'] = doc_topic_dist.idxmax(axis='columns')
        topics = self.get_topics()
        #print(comments.topic_id.values)
        #print(topics.iloc[1])
        #comments["topic"] = comments.topic_id.map(lambda t: topics.iloc[int(t)]['topkwords'])
        comments["topic"] = [ 'others' if np.isnan(t) else topics.iloc[t]['topkwords'] for t in comments.topic_id.values ]
        #comments["topic"] = [ 'others' if np.isnan(t) else 'topic' + str(t) for t in comments.topic_id.values ]
        return comments

    def get_topic_word_dist(self, topic):
        """
        Returns a dictionary mapping each word to its probability under the topic-word distribution of the topic.

        :param   int  The topic number as indicated by its topic_id.

        :return: dict A mapping of word to likelihood under topic-word distribution.
        """
        topic = int(topic)
        print(topic)
        with open('output_HMDP/{}/topktopics'.format(self.RUNS), 'r') as f:
            reader = list(csv.reader(f))
            dict_ = dict(zip(reader[2*topic][:-1], [float(p) for p in reader[2*topic+1][:-1]]))
        return dict_

    def get_bigram_labels(self, comments, output):
        # TODO: refactor
        df = self.get_topics()
        k = len(df.index)

        filter_ = lambda word1, word2: len({word1, word2}.intersection(set(words.split(" ")))) == 0

        for topic in range(k):

            words = comments[comments["topic_id"] == topic]["topic"].iloc[0]
            twdist = self.get_topic_word_dist(topic)

            # find bigrams from comments
            tokenizer = RegexpTokenizer(r'\w+')
            bigrams = nltk.collocations.BigramCollocationFinder.from_words(
                #get_words(clusters[topic]["comments"])
                " ".join(comments[comments["topic_id"] == topic].processed.apply(lambda text: " ".join(
                    tokenizer.tokenize(text))).str.lower().tolist()).split(" ")
            )

            # filtering of bigrams with no intersection with the top K words of the topic
            bigrams.apply_ngram_filter(filter_)
            bigram_measures = nltk.collocations.BigramAssocMeasures()
            # filtering of infrequent bigrams for performance
            top = bigrams.nbest(bigram_measures.raw_freq , 1000)

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
                scores = pd.DataFrame(columns=["bigram", "score"])

                for i, tpl in enumerate(top):
                    scores.at[i, "bigram"] = tpl
                    scores.at[i, "score"] = score(tpl)

                labels = scores[scores.score == scores.score.max()]
                comments.loc[comments["topic_id"] == topic, "topic"] = " ".join(
                    (labels.sample(1) if len(labels) > 1 else labels)["bigram"].iloc[0])

                print((labels.sample(1) if len(labels) > 1 else labels)["bigram"].iloc[0], file=open(output, "a"))

        return comments

    def get_trigram_labels(self, comments, output):
        # TODO: refactor
        df = self.get_topics()
        k = len(df.index)

        filter_ = lambda word1, word2, word3: len({word1, word2, word3}.intersection(set(words.split(" ")))) == 0

        for topic in range(k):

            words = comments[comments["topic_id"] == topic]["topic"].iloc[0]
            twdist = self.get_topic_word_dist(topic)

            # find bigrams from comments
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
            top = trigrams.nbest(trigram_measures.raw_freq , 1000)

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

                print((labels.sample(1) if len(labels) > 1 else labels)["trigram"].iloc[0], file=open(output, "a"))

        return comments
