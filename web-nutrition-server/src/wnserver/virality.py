
import tweepy
from newspaper import Article
import datetime
from lxml.html import document_fromstring
from lxml.etree import tostring
from itertools import chain

from nutrition.structure.environment import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, \
    TWITTER_ACCESS_TOKEN_SECRET
from wnserver.response import Label, SubFeature, SubFeatureError


class Virality(object):

    debug = False

    def __init__(self):
        # Creating the authentication object
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)

        # Setting your access token and secret
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

        # Creating the api object
        self.api = tweepy.API(auth)

    def get_max_tweet_rate(self, title, time_window=24*3600):
        results = tweepy.Cursor(self.api.search, q=title).items(300)

        timestamps = [result.created_at for result in results]
        start = 0
        end = 0  # exclusive

        tweet_max = 0
        while end < len(timestamps):
            while end < len(timestamps) and (timestamps[start] - timestamps[end]).total_seconds() < time_window:
                end += 1

            tweet_max = max(tweet_max, end - start)
            start += 1

        print(tweet_max)

        return tweet_max

    def get_virality(self, title):
        if self.debug:
            print(title)

        subfeatures = []
        if title:
            tweets_per_day = self.get_max_tweet_rate(title)
            main_score = 100 - 1000 / (tweets_per_day + 10)
            # if (tweets_per_day > 100):
            #     virality = 100
            # else:
            #     virality = tweets_per_day

            subfeatures.append(SubFeature('Tweets per day', tweets_per_day, tooltip='Tweet and retweet rate'))
        else:
            print('Failed to retrieve title')
            main_score = 0
            subfeatures.append(SubFeatureError('Tweets per hour'))

        if self.debug:
            print('title = ' + title)
            print('tweets per hour = ', tweets_per_day)

        return Label(main_score, subfeatures)


if __name__ == '__main__':
    virality = Virality()

    urls = [
        'https://edition.cnn.com/2018/07/10/football/cristiano-ronaldo-real-madrid-juventus-spt-intl/index.html'
    ]

    # article = Article('http://www.foxnews.com/politics/2018/06/25/intern-who-cursed-at-trump-is-identified-was-suspended-but-not-fired.html')

    for url in urls:
        article = Article(url)
        # print('downloading')

        article.download()
        if article.download_state == 0: #ArticleDownloadState.NOT_STARTED is 0
            print('Failed to retrieve')

        article.parse()
        label = virality.get_virality(article.title)

        # print('virality = ', score)
        print("{:<50}".format(article.title[:50]), label.dict)

