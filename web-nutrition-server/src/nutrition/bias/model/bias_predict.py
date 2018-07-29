#! usr/bin/env python
# *-- coding : utf-8 --*

import os
import pickle
import requests
from newspaper import Article
from nutrition.bias.model.content_model_text_functions import clean
from nutrition.structure.environment import BIAS_DATADIR, BIAS_URLS, BIAS_MODEL


class NewsBias(object):

    def __init__(self):
        self.datadir = BIAS_DATADIR
        self.model_objects = BIAS_MODEL
        self.urls = BIAS_URLS

    def predict_bias(self,newstext):
        for i, url in enumerate(self.urls):
            if not os.path.exists(self.datadir + '/' + self.model_objects[i]):
                self.download(url,i)

        bestclf = pickle.load(open(self.datadir + '/' + self.model_objects[0], 'rb'))
        besttfidf = pickle.load(open(self.datadir + '/' +  self.model_objects[1], 'rb'))

        #article = current_article.append(str(newstext))
        clean_article = clean(newstext)
        #print(clean_article)
        article_tfidf = besttfidf.transform([clean_article])
        if bestclf.predict(article_tfidf) == 0:
            return 0
        if bestclf.predict(article_tfidf) == 1:
            return  100
        else:
            return -1

    def download(self,url,i):
        r = requests.get(url, stream=True)
        with open(self.datadir + '/' + self.model_objects[i], 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)


def main():
    url = 'http://www.foxnews.com/politics/2018/06/25/intern-who-cursed-at-trump-is-identified-was-suspended-but-not-fired.html'
    news_bias = NewsBias()

    article = Article(url)
    # print('downloading')

    article.download()
    if article.download_state == 0:  # ArticleDownloadState.NOT_STARTED is 0
        print('Failed to retrieve')

    article.parse()
    label = news_bias.predict_bias(article.text)
    print(label)


if __name__ == '__main__':
    main()