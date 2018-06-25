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

    def get_influence(self, query):
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
        google_pagerank = float(str(scores['Google PageRank']).split('/')[0])*10
        cPR_Score = float(str(scores['cPR Score']).split('/')[0])*10
        followers_count = float(scores['followers_count'])*100/(float(thresh_hold_avg['followers_count'])/threshold_records)
        WOT_Score = float(str(scores['WOT Score']).split('/')[0])
        listed_count = float(scores['listed_count'])*100/(float(thresh_hold_avg['listed_count'])/threshold_records)
        alexa_rank = (1/(math.log((float(scores['Alexa Rank'].replace(',', '')))**0.0001)+0.01))
        source_influence = (friends_count + google_pagerank + cPR_Score +followers_count + WOT_Score + listed_count + alexa_rank)/7

        return {
            'main_score': source_influence,
            'web_of_trust': WOT_Score,
            'google_page_rank': google_pagerank,
            'cpr_score': cPR_Score,
            'alexa_rank': alexa_rank,
            'twitter_follower_count': followers_count,
            'twitter_friends_count': friends_count,
            'twitter_listed_count': listed_count
        }

    def emptytozero(self,input_string):
        if input_string == '':
            return '0'
        else:
            return input_string


if __name__ == '__main__':
    cred_obj = CredFeatures()

    extract_domain = tldextract.extract('https://www.nbcnews.com/storyline/immigration-border-crisis/where-s-my-kid-texas-border-desperate-parents-turn-attorneys-n886181')
    tld = extract_domain.domain + '.' + extract_domain.suffix
    print(cred_obj.get_influence(tld))

