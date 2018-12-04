from textblob import TextBlob
import re
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
from matplotlib import pyplot as plt

def clean_tweet(tweet):
    '''
    Utility function to clean the text in a tweet by removing
    links and special characters using regex.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

data = pd.read_json(open('Tweets_Cork_2018-05-03 15:32:57 2.json'))

tcount = pd.Series(data=1, index=data['created_at'])
tcount = tcount.resample('3H').sum()

# text
sentiment = [ clean_tweet(tweet) for tweet in data['full_text'] ]
text = ' '.join(sentiment)

stopwords = set(STOPWORDS)
stopwords.add("RT")
stopwords.add("got")

# Generate a word cloud image
#wordcloud = WordCloud(stopwords=stopwords).generate(text)

# Display the generated image:
#plt.imshow(wordcloud, interpolation='bilinear')
#plt.axis("off")


# lower max_font_size
wordcloud = WordCloud(stopwords=stopwords, max_font_size=60, width=1200, height=600).generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.tight_layout(pad=0)
plt.savefig('wordcloud')
