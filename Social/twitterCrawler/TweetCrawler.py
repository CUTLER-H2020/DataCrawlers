# -*- coding: utf-8 -*-
import os
from TwitterSearch import *
from dotenv import load_dotenv
from datetime import datetime
import csv
import sys
import json

class TweetCrawler:
    """ A class for tweet retrieval

    This class can be used to retrieve tweets around Cork or with relevant
    keywords
    The flag -g specifies, that tweets in a 20 mile radius around Fort Meagher
    are searched
    The flag -k specifies, that tweets with the keywords in CORK_KEYWORDS
    are searched
    """
    load_dotenv('.env')

    TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
    TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
    TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

    ANTALYA = {'keywords': ['Düden', '#Düden', '@antalyabb', 'from:antalyabb',
                            'to:antalyabb', 'Antalya', '#Antalya'],
               'geocode' : [36.852569, 30.782124],
               'name': 'Antalya'}

    ANTWERPEN = {'keywords': ['Antwerpen', '#Antwerpen', '@Stad_Antwerpen',
                              'to:Stad_Antwerpen', '@StadsLab2050', 'to:StadsLab2050',
                              '@DgplsAntwerpen', 'to:DgplsAntwerpen', '@DeZomer',
                              'to:DeZomer', '@LPAntwerpen', 'to:LPAntwerpen', '@PortofAntwerp',
                              'to:PortofAntwerp', '@SlimnaarA', 'to:SlimnaarA',
                              '@BZAntwerpen', 'to:BZAntwerpen', '@BusinessInA',
                              'to:BusinessInA'],
                 'geocode': [51.258820, 4.355700],
                 'name': 'Antwerpen'}

    CORK = {'keywords': ['Fort Meagher', 'Cork', 'Crosshaven', 'Camden Fort',
                         '#Cork', '#FortMeagher','#Crosshaven', '#lovecork',
                         '#purecork', '#visitCork', '@Corkcoco',
                         'from:Corkcoco', 'to:Corkcoco'],
            'geocode': [51.809083, -8.279279],
            'name': 'Cork'}

    THESSALONIKI = {'keywords': ['#Thessaloniki', 'Thessaloniki', '#Thermaikos',
                                 'Thermaikos', '@ThessalonikCity',
                                 'to:ThessalonikCity', '@AtThessaloniki'],
                    'geocode': [40.563893, 23.024136],
                    'name': 'Thessaloniki'}
    
    CITIES = [ANTALYA, ANTWERPEN, CORK, THESSALONIKI]

    def __init__(self):
        """
        Ensures, that the necessary access settings are set and creates
        TwitterSearchOrder instance for further search options
        """
        self.ts = TwitterSearch(
            consumer_key=self.TWITTER_CONSUMER_KEY,
            consumer_secret=self.TWITTER_CONSUMER_SECRET,
            access_token=self.TWITTER_ACCESS_TOKEN,
            access_token_secret=self.TWITTER_ACCESS_TOKEN_SECRET
        )
        self.tso = TwitterSearchOrder()

    def get_by_location(self, city):
        """
        Retrieves tweets in a 20 mile radius around Fort Meagher
        :param: Dict
        :return: None
        """
        # keywords serve as a placeholder, as empty keywords are not allowed in
        # TwitterSearch
        self.tso.set_keywords([" ", ".", ","], or_operator = True)
        self.tso.set_geocode(
            #self.CORK_GEOCODE_METRICS[0],
            #self.CORK_GEOCODE_METRICS[1],
            city['geocode'][0],
            city['geocode'][1],
            20,
            imperial_metric=True
            )
        self.get_tweets(city)

    def get_by_keywords(self, city):
        """
        Retrieves tweets according to the Keywords in CORK_KEYWORDS
        :return: None
        """
        #self.tso.set_keywords(self.CORK_KEYWORDS, or_operator = True)
        self.tso.set_keywords(city['keywords'], or_operator = True)
        self.get_tweets(city)

    def get_tweets(self, city):
        """
        Retrieves and saves tweets in a file.
        The options used for retrieval are saved in the tso object of the
        TweetCrawler instance
        :return: None
        """
        output_dir = 'outputs'
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
        # file for the shortened csv
        filename = 'Tweets_' + city['name'] + '_' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") \
                   + '.csv'
        # file for the json containing the entire retrieved information
        filename_raw = 'Tweets_'  + city['name'] + '_' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") \
                      + '.json'

        try:
            self.tso.set_language('en')
            # this option ensures, that tweets are not truncated
            self.tso.arguments.update({'tweet_mode': 'extended'})
            # self.tso.set_include_entities(False) # provides entity information

            with open(os.path.join(output_dir, filename), 'w') as f:
                tweets = []
                csvWriter = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
                csvWriter.writerow(['user', 'tweet'])
                for tweet in self.ts.search_tweets_iterable(self.tso):
                    csvWriter.writerow([
                        tweet['user']['screen_name'].encode('utf-8'),
                        tweet['full_text'].encode('utf-8')
                    ])
                    # this is more of a workaround as using the noniterable
                    # option of TwitterSearch 'search_tweets(tso)' caps the
                    # amount of retrieved tweets
                    tweets.append(tweet)
                # writes the total number of retrieved tweets at the end
                csvWriter.writerow(['tweets', len(tweets)])
            print("Retrieved Tweets in: " + output_dir + "/" + filename)

            # writes the entire data collected into a .json file
            with open(os.path.join(output_dir, filename_raw), 'w') as f_raw:
                json.dump(tweets, f_raw)

        except TwitterSearchException as e:
            print(e)
        except:
            print('Unexpected error: ' + sys.exc_info()[0])


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise IOError('Number of flags is faulty, specify exactly one flag.'
                      ' Use -g for geocode or -k for keywords.' )
    tc = TweetCrawler()
    flag = sys.argv[1]
    for city in tc.CITIES:
        if flag == '-g':
            tc.get_by_location(city)
        elif flag == '-k':
            tc.get_by_keywords(city)
        else:
            raise IOError('Flag is invalid. Use -g for geocode or -k for keywords')
