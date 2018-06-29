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
from nutrition.structure import environment


class CredFeatures(object):

    def __init__(self):
        self.__avail_scores = environment.SRC_FOLDER + '/nutrition/influence/data/available_scores'
        self.__threshold_score = environment.SRC_FOLDER + '/nutrition/influence/data/threshold_score'
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

    def get_influence(self, url):
        extract_domain = tldextract.extract(url)
        query = extract_domain.domain + '.' + extract_domain.suffix

        scores = self.get_features(query)
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

        if 'Google PageRank' in scores:
            google_pagerank = float(str(scores['Google PageRank']).split('/')[0])*10
        else:
            google_pagerank = 0

        if 'cPR Score' in scores:
            cPR_Score = float(str(scores['cPR Score']).split('/')[0])*10
        else:
            cPR_Score = 0

        followers_count = float(scores['followers_count'])*100/(float(thresh_hold_avg['followers_count'])/threshold_records)

        if 'WOT Score' in scores:
            WOT_Score = float(str(scores['WOT Score']).split('/')[0])
        else:
            WOT_Score = 0

        listed_count = float(scores['listed_count'])*100/(float(thresh_hold_avg['listed_count'])/threshold_records)

        if 'Alexa Rank' in scores:
            alexa_rank = (1/(math.log((float(scores['Alexa Rank'].replace(',', '')))**0.0001)+0.01))
        else:
            alexa_rank = 0

        source_influence = (friends_count + google_pagerank + cPR_Score +followers_count + WOT_Score + listed_count + alexa_rank)/7

        return {
            'main_score': source_influence,

            'subfeatures': [{
                'name': 'Web of Trust',
                'percentage': WOT_Score,
                'value': WOT_Score
            }, {
                'name': 'Alexa Rank',
                'percentage': alexa_rank,
                'value': alexa_rank
            }, {
                'name': 'Google Page Rank',
                'percentage': google_pagerank,
                'value': google_pagerank
            }, {
                'name': 'CheckPageRank.net Score',
                'percentage': cPR_Score,
                'value': cPR_Score
            }, {
                'name': 'Twitter followers',
                'percentage': followers_count,
                'value': followers_count
            }, {
                'name': 'Twitter friends',
                'percentage': friends_count,
                'value': friends_count
            }, {
                'name': 'Twitter listed',
                'percentage': listed_count,
                'value': listed_count
            }]
        }


if __name__ == '__main__':
    cred_obj = CredFeatures()

    print(cred_obj.get_influence('https://edition.cnn.com/2018/06/28/politics/joe-crowley-nancy-pelosi-alexandria-ocasio-cortez/index.html'))

