#! usr/bin/env python

import sys
import tldextract
import codecs
import ast
import math
from datetime import datetime
from nutrition.influence.scrapers.page_rank import PageRank
from nutrition.influence.scrapers.tweeter_metrics import ExtractAuthFeatures
import nutrition.influence.scrapers.web_trust_score as wts


class CredFeatures(object):

    def __init__(self):
        self.__avail_scores = '../data/available_scores'
        self.__threshold_score = '../data/threshold_score'
        self.pr = PageRank()
        self.twit_feat = ExtractAuthFeatures()

    def get_features(self, query):
        with codecs.open(self.__avail_scores, 'r', 'utf-8') as available_scores:
            for line in available_scores:
                tokens = line.split('|')
                if tokens[0] == str(datetime.today().date()):
                    if tokens[1] == query.strip().lower():
                        return ast.literal_eval(tokens[2])
        scores = wts.get_rank(query)
        for key, value in self.pr.get_rank(query).items():
            scores[key] = value
        for key, value in self.twit_feat.get_tweets(query).items():
            scores[key] = value
        with codecs.open(self.__avail_scores, 'a', 'utf-8') as write_scores:
            write_scores.write(str(datetime.today().date())+'|'+str(query.strip().lower()) + '|' + str(scores)+'\n')
        return scores

    def send_format(self, scores):
        """
        Normalized with google scores
        :param scores:
        :return:
        """
        thresh_hold_avg = {}
        thresh_hold_avg['followers_count'] = 0
        thresh_hold_avg['listed_count'] = 0
        thresh_hold_avg['friends_count'] = 0
        threshold_records = 0
        with codecs.open(self.__threshold_score, 'r', 'utf-8') as thresholding:
            for line in thresholding:
                tokens = line.split('|')
                threshold_scores = ast.literal_eval(tokens[2])
                thresh_hold_avg['friends_count'] += threshold_scores['friends_count']
                thresh_hold_avg['listed_count'] += threshold_scores['listed_count']
                thresh_hold_avg['followers_count'] += threshold_scores['followers_count']
                threshold_records += 1
        friends_count = float(scores['friends_count'])*100/(float(thresh_hold_avg['friends_count'])/threshold_records)
        google_pagerank = float(str(scores['Google PageRank']).split('/')[0])*10
        cPR_Score = float(str(scores['cPR Score']).split('/')[0])*10
        followers_count = float(scores['followers_count'])*100/(float(thresh_hold_avg['followers_count'])/threshold_records)
        WOT_Score = float(str(scores['WOT Score']).split('/')[0])
        listed_count = float(scores['listed_count'])*100/(float(thresh_hold_avg['listed_count'])/threshold_records)
        alexa_rank = (1/(math.log((float(scores['Alexa Rank'].replace(',', '')))**0.0001)+0.01))
        source_influence = (friends_count + google_pagerank + cPR_Score +followers_count + WOT_Score + listed_count + alexa_rank)/7

        return {'nutrition': [
                {
                    "name": "friends_count",
                    "display": "friends_count: " + str(round(friends_count)) + "%",
                    "value": scores['friends_count'],
                    "percentage": friends_count,
                    "color": "#0cc"
                },
                {
                    "name": "Google PageRank",
                    "display": "Google PageRank: " + str(round(google_pagerank)) + "%",
                    "value": scores['Google PageRank'],
                    "percentage": google_pagerank,
                    "color": "#0bc"
                },
                {
                    "name": "cPR_Score",
                    "display": "cPR_Score: " + str(round(cPR_Score)) + "%",
                    "value": scores['cPR Score'],
                    "percentage": cPR_Score,
                    "color": "#0dc"
                },
                {
                    "name": "followers_count",
                    "display": "followers_count: " + str(round(followers_count)) + "%",
                    "value": scores['followers_count'],
                    "percentage": followers_count,
                    "color": "#0ec"
                },
                {
                    "name": "WOT_Score",
                    "display": "WOT_Score: " + str(round(WOT_Score)) + "%",
                    "value": scores['WOT Score'],
                    "percentage": WOT_Score,
                    "color": "#0fc"
                },
                {
                    "name": "listed_count",
                    "display": "listed_count: " + str(round(listed_count)) + "%",
                    "value": scores['listed_count'],
                    "percentage": listed_count,
                    "color": "#0ac"
                },
                {
                    "name": "alexa_rank",
                    "display": "alexa_rank: " + str(round(alexa_rank, 2)) + "%",
                    "value": scores['Alexa Rank'],
                    "percentage": alexa_rank,
                    "color": "#0ac"
                },
                {
                    "name": "source_influence",
                    "display": "source_influence: " + str(round(source_influence)) + "%",
                    "value": source_influence,
                    "percentage": source_influence,
                    "color": "#0ac"
                },
            ]}

    def emptytozero(self,input_string):
        if input_string == '':
            return '0'
        else:
            return input_string


def main():
    cred_obj = CredFeatures()

    extract_domain = tldextract.extract('https://in.reuters.com/article/usa-immigration-trump/trump-says-illegal-immigrants-should-be-deported-with-no-judges-or-court-cases-idINKBN1JK0OR')
    tld = extract_domain.domain + '.' + extract_domain.suffix
    print(tld)
    print(type(tld))
    scores = cred_obj.get_features(tld)
    print(scores)
    finals = cred_obj.send_format(scores)
    print(finals['nutrition'])
    for key, value in scores.items():
        print("{}:{}".format(key, value))


if __name__ == '__main__':
    main()

