
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

        subfeatures = []
        if title:
            tweets_per_hour = self.get_tweets_per_hour(title)
            main_score = 100 - 1000 / (tweets_per_hour + 10)
            # if (tweets_per_hour > 100):
            #     virality = 100
            # else:
            #     virality = tweets_per_hour

            subfeatures.append(SubFeature('Tweets per hour', tweets_per_hour))
        else:
            print('Failed to retrieve title')
            main_score = 0
            subfeatures.append(SubFeatureError('Tweets per hour'))

        if self.debug:
            print('title = ' + title)
            print('tweets per hour = ', tweets_per_hour)

        return Label(main_score, subfeatures)


if __name__ == '__main__':
    virality = Virality()

    urls = [
        'https://www.nytimes.com/2018/06/26/us/politics/supreme-court-trump-travel-ban.html',
        'https://www.npr.org/2018/06/26/606427673/supreme-court-sides-with-california-anti-abortion-pregnancy-centers',
        'https://www.cnbc.com/2018/06/26/trump-says-harley-davidson-using-trade-tensions-as-an-excuse.html',
        'https://www.teslarati.com/tesla-model-3-summon-feature-video/',
        'https://venturebeat.com/2018/06/25/openai-cofounder-greg-brockman-on-the-transformative-potential-of-artificial-general-intelligence/',
        'https://finance.yahoo.com/news/ex-googler-pawned-her-24-192958661.html',
        'https://www.invenglobal.com/articles/5433/tl-doublelift-reveals-his-thoughts-on-imaqtpie-hitting-d1-his-future-and-the-meta',
        'https://www.anandtech.com/show/13010/realtek-nvme-pcie-rts5762-rts5763dl-controllers',
        'http://www.foxnews.com/politics/2018/06/25/intern-who-cursed-at-trump-is-identified-was-suspended-but-not-fired.html',
        'https://www.nytimes.com/2018/06/26/us/reality-winner-nsa-leak-guilty-plea.html'
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

