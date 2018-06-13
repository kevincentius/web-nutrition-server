
import tweepy
from newspaper import Article
import datetime
from lxml.html import document_fromstring
from lxml.etree import tostring
from itertools import chain

from nutrition.structure.environment import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, \
    TWITTER_ACCESS_TOKEN_SECRET


class Virality(object):

    debug = False

    def __init__(self):
        # Creating the authentication object
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)

        # Setting your access token and secret
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

        # Creating the api object
        self.api = tweepy.API(auth)


    def get_tweets_per_hour(self, title):
        results = tweepy.Cursor(self.api.search, q=title).items(100)
        time_array = []
        count = 1
        for tweet in results:
            if self.debug:
                print(tweet)
                print(count, tweet.created_at, tweet.text)
                count = count + 1

            time_array.append(tweet.created_at)
        if len(time_array) > 1:
            timespan = datetime.datetime.now() - time_array[len(time_array) - 1]
            tweets_per_hour = len(time_array) * 3600 / timespan.total_seconds()
        else:
            tweets_per_hour = 0
        return tweets_per_hour

    def get_virality(self, title):
        if self.debug:
            print(title)

        if title:
            tweets_per_hour = self.get_tweets_per_hour(title)
            virality = 100 - 1000 / (tweets_per_hour + 10)
        else:
            print('Failed to retrieve title')
            tweets_per_hour = 0
            virality = 0

        if self.debug:
            print('title = ' + title)
            print('tweets per hour = ', tweets_per_hour)

        return [virality, tweets_per_hour]


if __name__ == '__main__':
    virality = Virality()
    article = Article('https://www.politico.com/story/2018/06/12/navarro-comments-justin-trudeau-mistake-639075')

    print('downloading')

    article.download()
    if article.download_state == 0: #ArticleDownloadState.NOT_STARTED is 0
        print('Failed to retrieve')

    score = virality.get_virality(article.html)

    print('virality = ', score)

