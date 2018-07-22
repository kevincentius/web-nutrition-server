from datetime import datetime

import tweepy
from newspaper import Article
from math import log10

from pymongo import MongoClient

from nutrition.structure.environment import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, \
    TWITTER_ACCESS_TOKEN_SECRET
from wnserver.response import Label, SubFeature, SubFeatureError

import time

class Virality(object):

    debug = False
    update_interval = 15*60

    def __init__(self):
        # Creating the authentication object
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)

        # Setting your access token and secret
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

        # Creating the api object
        self.api = tweepy.API(auth)

    def get_max_tweet_rate(self, title, time_window=24*3600, limit=300):
        results = tweepy.Cursor(self.api.search, q=title).items(limit)

        timestamps = [result.created_at for result in results]
        if len(timestamps) == 0:
            return 0, time.time()

        time_span = (timestamps[0] - timestamps[-1]).total_seconds()
        peak_date = (timestamps[0].timestamp() + timestamps[-1].timestamp()) / 2

        if len(timestamps) == limit and time_span < time_window:
            # We get n tweets over less than 24 hours time span (viral)
            tweet_max = len(timestamps) * time_window / time_span

        elif len(timestamps) < limit and time_span < time_window:
            # We get less than n tweets over less than 24 hours time span
            # -> can be a non viral article
            # -> can be a new article
            tweet_max = len(timestamps) / limit
            # tweet_max = len(timestamps) * time_window / (datetime.utcnow() - timestamps[-1]).total_seconds()

        else:
            start = 0
            end = 0  # exclusive

            tweet_max = 0
            while end < len(timestamps):
                while end < len(timestamps) and (timestamps[start] - timestamps[end]).total_seconds() < time_window:
                    end += 1

                tweet_max = max(tweet_max, end - start)
                peak_date = (timestamps[end-1].timestamp() + timestamps[start].timestamp()) / 2
                start += 1

        return tweet_max, peak_date

    def get_virality(self, url, title):
        if self.debug:
            print(title)

        client = MongoClient()
        db = client.webNutritionDB.virality
        entry = db.find_one({"url": url})

        tweets_per_day = 0
        if entry and (time.time() - entry['timestamp']) < Virality.update_interval:
            # fresh data in database --> take value from db
            tweets_per_day = entry['tweets_per_day']
            peak_date = entry['peak_date']
        else:
            # old or no data in database --> calculate
            tweets_per_day, peak_date = self.get_max_tweet_rate(title)

            if entry and entry['tweets_per_day'] >= tweets_per_day:
                tweets_per_day = entry['tweets_per_day']
                peak_date = entry['peak_date']

        # update database
        if not entry or entry['tweets_per_day'] < tweets_per_day:
            db.update_one({"url": url}, {"$set": {
                "timestamp": time.time(),
                "tweets_per_day": tweets_per_day,
                "peak_date": peak_date,
                "title": title
            }}, True)

        if self.debug:
            print('title = ' + title)
            print('tweets per day = ', tweets_per_day)

        # build response
        subfeatures = []
        main_score = min(100.0, 73 * log10(tweets_per_day/24 + 1))
        tooltip = 'There were estimated ' + str(tweets_per_day) + ' tweets/retweets on ' + datetime.fromtimestamp(peak_date).strftime("%d/%m/%Y")
        subfeatures.append(
            SubFeature('Tweets per day', tweets_per_day, main_score, tooltip=tooltip))

        return Label(main_score, subfeatures)


if __name__ == '__main__':
    virality = Virality()

    urls = [
        'https://www.reuters.com/article/us-usa-russia-summit-trump/trump-tries-to-calm-political-storm-over-putin-summit-says-he-misspoke-idUSKBN1K72FL'
    ]

    # article = Article('http://www.foxnews.com/politics/2018/06/25/intern-who-cursed-at-trump-is-identified-was-suspended-but-not-fired.html')

    for url in urls:
        article = Article(url)
        # print('downloading')

        article.download()
        if article.download_state == 0: #ArticleDownloadState.NOT_STARTED is 0
            print('Failed to retrieve')

        article.parse()
        label = virality.get_virality(url, article.title)

        # print('virality = ', score)
        print("{:<50}".format(article.title[:50]), label.dict)

