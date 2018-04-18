
from newspaper import Article
from textstat.textstat import textstat


class Analyzer(object):

    def analyze(self, url):
        article = Article(url)
        
        print('downloading', url)
        print(article.download())
        if article.download_state == 0: #ArticleDownloadState.NOT_STARTED is 0
            return {'error': 'Failed to retrieve from ' + url}
        
        article.parse()
        if not article.text:
            return {'error': 'Failed to parse document'}
            
        print(article.text.encode("utf-8"))
        
        readability = textstat.flesch_reading_ease(article.text)
        
        # readability + some mock data
        return {'nutrition': [
            {
                "name": "readability",
                "display": "readability",
                "value": readability,
                "color": "#f00"
            },
            {
                "name": "topicality",
                "display": "topicality",
                "value": 50,
                "color": "#fc0"
            },
            {
                "name": "factuality",
                "display": "factuality",
                "value": 50,
                "color": "#0f0"
            },
            {
                "name": "emotion",
                "display": "emotion",
                "value": 50,
                "color": "#0cc"
            },
            {
                "name": "authority",
                "display": "authority",
                "value": 50,
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
