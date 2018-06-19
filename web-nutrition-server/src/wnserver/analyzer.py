
from newspaper import Article
from textstat.textstat import textstat
from wnserver.readability import Readability
from wnserver.sentiment_and_subjectivity import Sentiment
from wnserver.virality import Virality
from wnserver.stopwatch import Stopwatch
import time
from concurrent.futures.thread import ThreadPoolExecutor
import traceback


class Analyzer(object):

    debug = True

    def __init__(self):
        self.virality = Virality()
        self.readability = Readability()
        self.sentiment = Sentiment()
        self.analyze_count = 0

    def call(self, func, *args):
        start_time = time.time()

        result = func(*args)
        if self.debug:
            print('{} returned {} in {:.2f} seconds'.format(func.__name__, result, time.time() - start_time))
        return result

    def get_result(self, future, name, default=None):
        exc = future.exception()
        if exc is None:
            result = future.result()
            return result
        else:
            if self.debug:
                print(name, 'threw exception', exc)
            return default

    def analyze(self, url):
        self.analyze_count += 1
        if self.debug:
            print('Stopwatch analyze ' + str(self.analyze_count) + ': ' + url)
            stopwatch = Stopwatch('analyze ' + str(self.analyze_count))
        
        article = Article(url)
        
        # download full page from url
        if self.debug:
            stopwatch.lap('downloading {}'.format(url))
        
        article.download()
        if article.download_state == 0: #ArticleDownloadState.NOT_STARTED is 0
            if self.debug:
                print('Failed to retrieve from ' + url)
            return {'error': 'Failed to retrieve from ' + url}

        # extract the main text content of the page
        if self.debug:
            stopwatch.lap('newspaper3k parsing')

        article.parse()
        if not article.text:
            if self.debug:
                print('newspaper3k parse failed on ' + url)
            return {'error': 'Failed to process document'}

        if self.debug:
            print(article.text.encode("utf-8"))

        # start nutrition label analysis in parallel
        if self.debug:
            stopwatch.lap('analzying nutrition labels')
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            f_readability = executor.submit(self.call, self.readability.get_readability, article.text)
            f_virality = executor.submit(self.call, self.virality.get_virality, article.title)
            f_sentiment = executor.submit(self.call, self.sentiment.get_sentiment, article.text)

        # read the results (error robustness: error in a label must not stop other labels from being delivered)
        readability = self.get_result(f_readability, 'readability', 0)
        [virality, tweets_per_hour] = self.get_result(f_virality, 'virality', [0, 0])
        [sentiment, subjectivity] = self.get_result(f_sentiment, 'sentiment', [0, 0])

        if self.debug:
            stopwatch.finish()

        gunning_fog = textstat.gunning_fog(article.text)
        
        # readability + some mock data
        return {'nutrition': [
            {
                "name": "readability",
                "display": "readability: " + str(round(readability)) + "%",
                "value": readability,
                "percentage": readability,
                "color": "#f00"
            },
            {
                "name": "virality",
                "display": "virality: {:.3g} tweets per hour".format(tweets_per_hour),
                "value": virality,
                "percentage": virality,
                "color": "#fc0"
            },
            {
                "name": "sentiment",
                "display": "sentiment: " + str(round((sentiment + 1) * 50)) + "%",
                "value": (sentiment + 1) * 50,
                "percentage": (sentiment + 1) * 50,
                "color": "#0f0"
            },
            {
                "name": "objectivity",
                "display": "objectivity: " + str(round((1-subjectivity) * 100)) + "%",
                "value": (1-subjectivity) * 100,
                "percentage": (1-subjectivity) * 100,
                "color": "#0cc"
            },
            {
                "name": "gunning_fog",
                "display": "gunning fog: " + str(round(gunning_fog)),
                "value": gunning_fog,
                "percentage": 100 - gunning_fog * 100 / 30,
                "color": "#00f"
            }
        ]}
    
    def dump(self, obj):
        for attr in dir(obj):
            print("obj.%s = %r" % (attr, getattr(obj, attr)))


if __name__ == "__main__":
    analyzer = Analyzer()
    print(analyzer.analyze('https://en.wikipedia.org/wiki/Chess'))
    #analyzer.analyze('http://money.cnn.com/2018/04/18/media/president-trump-media-protectors/index.html')
