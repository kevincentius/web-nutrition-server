
from newspaper import Article
from textstat.textstat import textstat
from server.readability import Readability
from server.virality import Virality
from server.stopwatch import Stopwatch
import time
from concurrent.futures.thread import ThreadPoolExecutor

class Analyzer(object):

    debug = True

    def __init__(self):
        self.virality = Virality()
        self.readability = Readability()

    def call(self, func, *args):
        try:
            start_time = time.time()
            
            result = func(*args)
            if self.debug:
                print('{} returned {:.0f} in {:.2f} seconds'.format(func.__name__, result, time.time() - start_time))
            return result
        except:
            print('error when calling', func)
            return 0

    def analyze(self, url):
        stopwatch = Stopwatch('analyze')
        
        article = Article(url)
        
        # download full page from url
        if self.debug:
            stopwatch.lap('downloading {}'.format(url))
        
        article.download()
        if article.download_state == 0: #ArticleDownloadState.NOT_STARTED is 0
            return {'error': 'Failed to retrieve from ' + url}
        
        # extract the main text content of the page
        if self.debug:
            stopwatch.lap('newspaper3k parsing')
            
        article.parse()
        if not article.text:
            return {'error': 'Failed to process document'}
        
        if self.debug:
            print(article.text.encode("utf-8"))
                
        # start nutrition label analysis in parallel
        if self.debug:
            stopwatch.lap('analzying nutrition labels')
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            f_readability = executor.submit(self.call, self.readability.get_readability, article.text)
            f_virality = executor.submit(self.call, self.virality.get_virality, article.html)

        readability = f_readability.result()
        virality = f_virality.result()

        if self.debug:
            stopwatch.finish()
            
        flesch_reading_ease = textstat.flesch_reading_ease(article.text)
        linsear_write_formula = textstat.linsear_write_formula(article.text)
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
                "display": "virality: " + str(round(virality)),
                "value": virality,
                "percentage": virality,
                "color": "#fc0"
            },
            {
                "name": "flesch_reading_ease",
                "display": "flesch reading ease: " + str(round(flesch_reading_ease)) + "%",
                "value": flesch_reading_ease,
                "percentage": flesch_reading_ease,
                "color": "#0f0"
            },
            {
                "name": "linsear_write_formula",
                "display": "linsear write formula: " + str(round(linsear_write_formula)),
                "value": linsear_write_formula,
                "percentage": 100 - linsear_write_formula * 100 / 20,
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
    analyzer.analyze('https%3A%2F%2Fgithub.com%2Fcodelucas%2Fnewspaper%2Fissues%2F357')
    #analyzer.analyze('http://money.cnn.com/2018/04/18/media/president-trump-media-protectors/index.html')
