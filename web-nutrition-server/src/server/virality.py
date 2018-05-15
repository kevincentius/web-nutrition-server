
import tweepy
from lxml import etree
from newspaper import Article
import lxml
from io import StringIO
import datetime

class Virality(object):

    debug = True

    def __init__(self):
        consumer_key = "RvBkfoQWrJIAWrG1Ih6VRDRB1"
        consumer_secret = "t8kjE5wptu2ktPKs3ui254acK2IbJPcgkKw31hAnweJsK85oMI"
        access_token = "959735476415549440-bhFGGPTWH6Z5W7ZKPEwadmXKPL4eG5M"
        access_token_secret = "3y2YgvOvUrrsT2AuSXy4FxpkxJ3xl4G5n9OaTDfxWkOVN"

        # Creating the authentication object
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        # Setting your access token and secret
        auth.set_access_token(access_token, access_token_secret)

        # Creating the api object
        self.api = tweepy.API(auth)

    def get_title(self, html):
        parser = etree.XMLParser(encoding='UTF-8', recover=True)
        tree = etree.parse(StringIO(html), parser)

        for i in range(1, 5):
            element = tree.find('//h' + str(i))
            if element is not None:
                return element.text

        return None;

    def get_tweets_per_hour(self, title):
        results = tweepy.Cursor(self.api.search, q=title).items(100)
        time_array = []
        count = 1
        for tweet in results:
            if Virality.debug:
                print(count, tweet.created_at, tweet.text)
                count = count + 1

            time_array.append(tweet.created_at)
        if len(time_array) > 1:
            timespan = datetime.datetime.now() - time_array[len(time_array) - 1]
            tweets_per_hour = len(time_array) * 3600 / timespan.total_seconds()
        else:
            tweets_per_hour = 0
        return timespan, tweets_per_hour

    def get_virality(self, html):
        title = self.get_title(html)
        timespan, tweets_per_hour = self.get_tweets_per_hour(title)
        virality = 100 - 1000 / (tweets_per_hour + 10)

        if Virality.debug:
            print('title = ' + title)
            print('timespan = ', timespan)
            print('tweets per hour = ', tweets_per_hour)

        return virality


if __name__ == '__main__':
    virality = Virality()
    article = Article('http://www.nydailynews.com/new-york/harlem-school-aide-dragged-kindergartner-stage-10m-suit-article-1.3991176')

    if Virality.debug:
        print('downloading')

    article.download()
    if article.download_state == 0: #ArticleDownloadState.NOT_STARTED is 0
        print('Failed to retrieve')

    score = virality.get_virality(article.html)

    if Virality.debug:
        print('virality = ', score)

