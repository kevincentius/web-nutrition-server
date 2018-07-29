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
from wnserver.database import Database
from wnserver.response import SubFeature, SubFeatureError, Label


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
        for key, value in self.twit_feat.get_tweets(query).items():
            scores[key] = value
        with codecs.open(self.__avail_scores, 'a', 'utf-8') as write_scores:
            write_scores.write(str(datetime.today().date())+'|'+str(query.strip().lower()) + '|' + str(scores)+'\n')
        return scores

    def get_influence(self, url):
        extract_domain = tldextract.extract(url)
        query = extract_domain.domain + '.' + extract_domain.suffix

        db = Database(collection='popularity')
        stored_result = db.find_result(query)

        if stored_result and 'popularity' in stored_result:
            return Label(ldict=stored_result['popularity'])

        scores = self.get_features(query)
        """
        Normalized with google scores
        :param scores:
        :return:
        """
        thresh_hold_avg = {}
        thresh_hold_avg['followers_count'] = 0
        thresh_hold_avg['listed_count'] = 0
        threshold_records = 0
        with codecs.open(self.__threshold_score, 'r', 'utf-8') as thresholding:
            for line in thresholding:
                tokens = line.split('|')
                threshold_scores = ast.literal_eval(tokens[2])
                thresh_hold_avg['listed_count'] += threshold_scores['listed_count']
                thresh_hold_avg['followers_count'] += threshold_scores['followers_count']
                threshold_records += 1

        subfeatures = []
        score_sum = 0
        score_count = 0
        if 'WOT Score' in scores:
            WOT_Score = float(str(scores['WOT Score']).split('/')[0])
            subfeatures.append(SubFeature('Web of Trust Score',
                                          WOT_Score,
                                          tooltip="Website safety score based on a crowdsourced reputation system."))

            score_sum += WOT_Score
            score_count += 1
        else:
            subfeatures.append(SubFeatureError('Web of Trust Score'))

        alexa_rank = self.pr.get_alexa_rank(query)
        subfeatures.append(alexa_rank)
        if alexa_rank is not SubFeatureError:
            score_sum += alexa_rank.dict['percentage']
            score_count += 1

        page_rank = self.pr.get_page_rank(query)
        subfeatures.append(page_rank)
        if page_rank is not SubFeatureError:
            score_sum += page_rank.dict['percentage']
            score_count += 1

        twitter_score = 0
        twitter_features = 0
        if 'followers_count' in scores:
            followers_count = float(scores['followers_count'])*100/(float(thresh_hold_avg['followers_count'])/threshold_records)
            twitter_score += followers_count
            twitter_features += 1

        if 'listed_count' in scores:
            listed_count = float(scores['listed_count'])*100/(float(thresh_hold_avg['listed_count'])/threshold_records)
            twitter_score += listed_count
            twitter_features += 1

        if twitter_features > 0:
            subfeatures.append(SubFeature('Twitter popularity', twitter_score / twitter_features,
                                          tooltip=str(scores['followers_count']) + ' followers, '
                                                 + str(scores['listed_count']) + ' times listed'))
            # score_sum += twitter_score/twitter_features
            # score_count += 1
        else:
            subfeatures.append(SubFeatureError('Twitter popularity'))

        label = Label(score_sum / score_count, subfeatures)
        db.upsert_result(query, 'popularity', label.dict)
        return label


if __name__ == '__main__':
    cred_obj = CredFeatures()

    print(cred_obj.get_influence('https://edition.cnn.com/2018/07/12/politics/two-trumps-nato/index.html').dict)

