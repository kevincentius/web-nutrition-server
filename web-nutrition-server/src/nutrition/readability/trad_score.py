# -*- coding: utf-8 -*-
"""
Created on Mon Mar 05 03:17:25 2018

@author: simha

This program file is used to calculate readability scores using traditional formulae.
These are also considered as lexical units.

These measures are extracted from textstat API, which was already built by others.
we can hack it though. These are just formulae and can be found in wikipedia.

"""
from __future__ import division
from textstat.textstat import textstat
import math
import operator


def legacy_round(number, points=0):
    p = 10 ** points
    return float(math.floor((number * p) + math.copysign(0.5, number))) / p


def rescale(value, new_min=0.0, new_max=100.0):
    # values = list(values)
    old_min = 5
    old_max = 13

    new_v = (new_max - new_min) / (old_max - old_min) * (value - old_min) + new_min
    output = new_v

    return output


def text_standard1(text):
    grade = []

    # Appending Flesch Kincaid Grade
    lower = legacy_round(textstat.flesch_kincaid_grade(text))
    upper = math.ceil(textstat.flesch_kincaid_grade(text))
    grade.append(int(lower))
    grade.append(int(upper))

    # Appending Flesch Reading Easy
    score = textstat.flesch_reading_ease(text)
    if score < 100 and score >= 90:
        grade.append(5)
        FRE_score = 5.0
    elif score < 90 and score >= 80:
        grade.append(6)
        FRE_score = 6.0
    elif score < 80 and score >= 70:
        grade.append(7)
        FRE_score = 7.0
    elif score < 70 and score >= 60:
        grade.append(8)
        FRE_score = 8.0
    elif score < 60 and score >= 50:
        grade.append(9)
        FRE_score = 9.0
    elif score < 50 and score >= 40:
        grade.append(10)
        FRE_score = 10.0
    elif score < 40 and score >= 30:
        grade.append(12)
        FRE_score = 12.0
    else:
        grade.append(13)
        FRE_score = 13.0

    # Appending SMOG Index
    lower = legacy_round(textstat.smog_index(text))
    upper = math.ceil(textstat.smog_index(text))
    grade.append(int(lower))
    grade.append(int(upper))

    # Appending Coleman_Liau_Index
    lower = legacy_round(textstat.coleman_liau_index(text))
    upper = math.ceil(textstat.coleman_liau_index(text))
    grade.append(int(lower))
    grade.append(int(upper))

    # Appending Automated_Readability_Index
    lower = legacy_round(textstat.automated_readability_index(text))
    upper = math.ceil(textstat.automated_readability_index(text))
    grade.append(int(lower))
    grade.append(int(upper))

    # Appending Dale_Chall_Readability_Score
    lower = legacy_round(textstat.dale_chall_readability_score(text))
    upper = math.ceil(textstat.dale_chall_readability_score(text))
    grade.append(int(lower))
    grade.append(int(upper))

    # Appending Linsear_Write_Formula
    lower = legacy_round(textstat.linsear_write_formula(text))
    upper = math.ceil(textstat.linsear_write_formula(text))
    grade.append(int(lower))
    grade.append(int(upper))

    # Appending Gunning Fog Index
    lower = legacy_round(textstat.gunning_fog(text))
    upper = math.ceil(textstat.gunning_fog(text))
    grade.append(int(lower))
    grade.append(int(upper))

    # Finding the Readability Consensus based upon all the above tests
    d = dict([(x, grade.count(x)) for x in grade])
    sorted_x = sorted(d.items(), key=operator.itemgetter(1))
    final_grade = str((sorted_x)[len(sorted_x) - 1])
    score = final_grade.split(',')[0].strip('(')
    # print "score: ",score
    if int(score) > 13:
        score = 13
    if int(score) < 5:
        score = 5

    #    lix_score = textstat.lix(text)
    #    if lix_score <= 25:
    #        lix = 5.0
    #    if lix_score > 25 and lix_score <=35:
    #        lix = 7.0
    #    if lix_score < 25:
    #        lix = 9.0
    #    if lix_score < 25:
    #        lix = 12.0
    #    if lix_score < 25:
    #        lix = 13.0

    scores = {'FRE_score': FRE_score,
              'FKG_score': textstat.flesch_kincaid_grade(text),
              'Coleman': textstat.coleman_liau_index(text),
              'ARE': textstat.automated_readability_index(text),
              'Dale_Chal': textstat.dale_chall_readability_score(text),
              'linsear': textstat.linsear_write_formula(text),
              'Gunning': textstat.gunning_fog(text)
              }

    # return [int(score),str(int(score)-1) + "th " + "and " + str(int(score)) + "th grade", rescale(int(score))]
    #    return [FRE_score,textstat.flesch_kincaid_grade(text),textstat.coleman_liau_index(text),
    #            textstat.automated_readability_index(text),textstat.dale_chall_readability_score(text),
    #            textstat.linsear_write_formula(text),
    #            textstat.gunning_fog(text),int(score)]
    #
    return [scores, float(score)]


def all_trad_scores(text):
    fre = textstat.flesch_reading_ease(text)
    fkg = textstat.flesch_kincaid_grade(text)
    smog = textstat.smog_index(text)
    cole = textstat.coleman_liau_index(text)
    ari = textstat.automated_readability_index(text)
    dale = textstat.dale_chall_readability_score(text)
    linsear = textstat.linsear_write_formula(text)
    gunning = textstat.gunning_fog(text)

    return [fre, fkg, smog, cole, ari, dale, linsear, gunning]


if __name__ == '__main__':
    test_data = """Eleven states working in conjunction with the U.S Department of Transportation (D.O.T) have agreed to implement an ordinance banning the use of electronic cigarettes in vehicles  meaning if you are a resident of one of the impacted states, you will be prohibited from utilizing an electronic cigarette while inside your vehicle."""
    print(all_trad_scores(test_data))
#
#    print textstat.flesch_reading_ease(test_data)
#    print textstat.smog_index(test_data)
#    print textstat.flesch_kincaid_grade(test_data)
#    print textstat.coleman_liau_index(test_data)
#    print textstat.automated_readability_index(test_data)
#    print textstat.dale_chall_readability_score(test_data)
#    print textstat.difficult_words(test_data)
#    print textstat.linsear_write_formula(test_data)
#    print textstat.gunning_fog(test_data)
#    print("score of the article: ",(text_standard1(test_data))[0])
#    print ((text_standard1(test_data))[1])
#    print('Equivaent score in percentage : ',text_standard1(test_data)[2])


# sentence = "ABC cites the fact that chemical additives are banned in many countries and feels they may be banned in this state too."
# textstat.smog_index(sentence)
# textstat.gunning_fog(sentence)
