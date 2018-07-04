# -*- coding: utf-8 -*-
"""
Created on Thu May 03 01:07:19 2018

@author: simha

given the text of an news article, this program informs quantity of the sentiments and
objectivity of the article.

we use Pattern Api to find the respective scores.

we are only intereseted in how sentimental the article is? For this reason we consider 
absolute values of the sentiment score which is originally spread [-1,1].

The opinion score is distributed over [0,1] higher the value more opinion oriented. 

"""
from newspaper import Article
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from pattern3.en import sentiment
from contractions import fix

from wnserver.response import SubFeature, Label


class Sentiment(object):

    def get_sentiment(self, text):
        positive_score = 0
        negative_score = 0
        neutral_count = 0
        positive_count = 0
        negative_count = 0
        subjectivity_sum = 0
        sents = sent_tokenize(text)
        sents_count = len(sents)
        sents[:] = [s.strip() for s in sents]
        sents[:] = filter(None, sents)
        sents[:] = [re.sub(r"\s?\(.*?\)", r"", s) for s in
                    sents]  # delete parentheses with inside - ex: Ali (Farid) => Ali
        sents[:] = [fix(s) for s in sents]
        sents[:] = [s.replace('\n', '').replace('|', '').replace("“", '').replace("”", '').replace('"', '').replace('$',
                                                                                                                    '').replace(
            "'", '').replace('/', ' ').replace("-", '') for s in sents]
        sents[:] = [s.strip().lower() for s in sents]
        for i in range(sents_count):
            result = sentiment(sents[i])
            sentiment_result = result[0]
            subjectivity_sum += result[1]
            if sentiment_result == 0.0:
                neutral_count += 1
            elif sentiment_result > 0:
                positive_count += 1
                positive_score += sentiment_result
            else:
                negative_count += 1
                negative_score += sentiment_result

        avg_positive_score = positive_score / sents_count * 100
        avg_negative_score = abs(negative_score) / sents_count * 100
        overall_score = avg_positive_score + avg_negative_score
        avg_objectivity = (1 - subjectivity_sum / sents_count) * 100

        return [
            # sentiment
            Label(overall_score, [
                SubFeature('Positive sentiment', avg_positive_score, avg_positive_score ** 0.4),
                SubFeature('Negative sentiment', avg_negative_score, avg_negative_score ** 0.4)
            ]),

            # objectivity
            Label(avg_objectivity, [])
        ]


if __name__ == "__main__":
    sentiment_and_subjectivity = Sentiment()
    article = Article('https://in.reuters.com/article/usa-immigration-trump/trump-says-illegal-immigrants-should-be-deported-with-no-judges-or-court-cases-idINKBN1JK0OR')
    article.download()
    article.parse()
    scores = sentiment_and_subjectivity.get_sentiment(article.text)
    print(scores[0].dict)
    print(scores[1].dict)
