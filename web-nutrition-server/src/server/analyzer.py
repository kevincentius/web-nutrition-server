
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
            return {'error': 'Failed to process document'}
            
        print(article.text.encode("utf-8"))
        
        readability = textstat.flesch_reading_ease(article.text)
        flesch_kincaid_grade = textstat.flesch_kincaid_grade(article.text)
        dale_chall_readability_score = textstat.dale_chall_readability_score(article.text)
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
                "name": "flesch_kincaid_grade",
                "display": "flesch kincaid grade: " + str(round(flesch_kincaid_grade)),
                "value": flesch_kincaid_grade,
                "percentage": 100 - flesch_kincaid_grade * 100 / 20,
                "color": "#fc0"
            },
            {
                "name": "dale_chall_readability_score",
                "display": "dale chall readability: " + str(round(dale_chall_readability_score)),
                "value": dale_chall_readability_score,
                "percentage": 100 - dale_chall_readability_score * 100 / 12,
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
