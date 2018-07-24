
from newspaper import Article
from textstat.textstat import textstat

from nutrition.influence.scrapers.credibility_features import CredFeatures
from wnserver.readability import Readability
from wnserver.response import Response, Label
from wnserver.sentiment_and_subjectivity import Sentiment
from wnserver.virality import Virality
from wnserver.stopwatch import Stopwatch
import time
from concurrent.futures.thread import ThreadPoolExecutor
from wnserver.database import Database
import traceback


class Analyzer(object):

    debug = True

    def __init__(self):
        self.virality = Virality()
        self.readability = Readability()
        self.sentiment = Sentiment()
        self.influence = CredFeatures()
        self.analyze_count = 0

    def call(self, func, *args):
        start_time = time.time()

        result = func(*args)
        if self.debug:
            print('{} returned {} in {:.2f} seconds'.format(func.__name__, result, time.time() - start_time))
        return result

    def ret(self, retval):
        return retval

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

        db = Database()
        stored_result = db.find_result(url)
        if stored_result is None:
            stored_result = {}

        with ThreadPoolExecutor(max_workers=5) as executor:
            f_virality = executor.submit(self.call, self.virality.get_virality, article.url, article.title)
            f_influence = executor.submit(self.call, self.influence.get_influence, url)

            if 'readability' in stored_result:
                f_readability = executor.submit(self.ret, Label(ldict=stored_result['readability']))
            else:
                f_readability = executor.submit(self.call, self.readability.get_readability, article.text)

            if 'sentiment' in stored_result and 'objectivity' in stored_result:
                f_sentiment = executor.submit(self.ret, [
                    Label(ldict=stored_result['sentiment']),
                    Label(ldict=stored_result['objectivity'])
                ])
            else:
                f_sentiment = executor.submit(self.call, self.sentiment.get_sentiment, article.text)

        # read the resu alts (error robustness: error in label must not stop other labels from being delivered)
        result_virality = self.get_result(f_virality, 'virality')
        result_readability = self.get_result(f_readability, 'readability')
        [result_sentiment, result_objectivity] = self.get_result(f_sentiment, 'sentiment', [None, None])
        result_influence = self.get_result(f_influence, 'influence')

        if 'readability' not in stored_result and result_readability is not None:
            db.upsert_result(url, 'readability', result_readability.dict)

        if 'sentiment' not in stored_result and result_sentiment is not None:
            db.upsert_result(url, 'sentiment', result_sentiment.dict)

        if 'objectivity' not in stored_result and result_objectivity is not None:
            db.upsert_result(url, 'objectivity', result_objectivity.dict)

        # build response
        response = Response({
            'readability': result_readability,
            'virality': result_virality,
            'sentiment': result_sentiment,
            'objectivity': result_objectivity,
            'source': result_influence
        })

        if self.debug:
            stopwatch.finish()


        return response.dict


if __name__ == "__main__":
    analyzer = Analyzer()
    print(analyzer.analyze('https://www.npr.org/2018/07/03/625603260/former-malaysian-prime-minister-arrested-amid-corruption-scandal'))
    #analyzer.analyze('http://money.cnn.com/2018/04/18/media/president-trump-media-protectors/index.html')
