from textblob import TextBlob
import re
import pandas as pd

from matplotlib import pyplot as plt

def clean_tweet(tweet):
    '''
    Utility function to clean the text in a tweet by removing
    links and special characters using regex.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

data = pd.read_json(open('Tweets_Cork_2018-05-03 15:32:57 2.json'))

tfav = pd.Series(data=data['favorite_count'].values, index=data['created_at'])
tret = pd.Series(data=data['retweet_count'].values, index=data['created_at'])

# aggregate
tfav = tfav.resample('3H').sum()
tfav[tfav == 0] = 1
tret = tret.resample('3H').sum()

tfav.plot(figsize=(16,4), label="Likes", marker="o", legend=True)
tret.plot(figsize=(16,4), label="Retweets", marker="o", legend=True)

plt.yscale('log')
plt.savefig('stats')

# sentiment
sentiment = [ TextBlob(clean_tweet(tweet)).sentiment.polarity for tweet in data['full_text'] ]
tsent = pd.Series(data=sentiment, index=data['created_at'])
tsent = tsent.resample('3H').mean()

# plot
plt.cla()
tsent.plot(figsize=(16,4), label="Sentiment", marker="o", legend=True, color='red')
plt.savefig('sentiment')
