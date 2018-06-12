# -*- coding: utf-8 -*-
"""
Created on Fri Apr 06 17:28:30 2018

@author: simha

This program file is used to extract various averaged lexical tokens per article
pattern and contractions APIs must be installed beforehand.
"""

from __future__ import division
from nltk.corpus import stopwords
import numpy as np
import math

from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import word_tokenize
from nltk import FreqDist
from contractions import fix


# txt = """Natural language processing (NLP) is a field of computer science, artificial intelligence, and computational linguistics concerned with the inter
# actions between computers and human (natural) languages."""


# sentence = "The brown fox wasn't that quick and he couldn't win the race."

# finding ngrams
from nutrition.readability import text_normalization as tn
from nutrition.structure.data_set import DataSet


def find_ngrams(input_list, n):
    return zip(*[input_list[i:] for i in range(n)])


# Extracting meaningful bigrams like United States Jon peter....
def count_meaningful_bigrams(annotation):
    count = 0
    for sentence in annotation['sentences']:
        tokens = sentence['tokens']
        for i in range(len(tokens) - 1):
            tag1 = tokens[i]['pos']
            tag2 = tokens[i+1]['pos']
            if tag1 in ['NNP', 'JJ', 'NN'] and tag2 in ['NN', 'NNP']:
                count += 1

    return count


# word complexity
def word_complexity(tokens):
    complex_words = filter(lambda z: len(z) > 4, tokens)


# type token ratios calcuations
def ttr_pos_entities(pos_words, all_words):
    n = len(all_words)
    t = len(pos_words)

    nttr = float(t) / n
    rttr = float(t) / (n ** 0.5)
    cttr = float(t) / ((2 * n) ** 0.5)
    mass = (math.log(n+1) - math.log(t+1)) / math.log(n+1) ** 2
    return [nttr, rttr, cttr, mass]


# type token ratios for different POS tags
def ttr_pos(annotation):
    tagged_sentences = [[(token['word'], token['pos']) for token in sentence['tokens']] for sentence in annotation['sentences']]

    nouns = []
    verbs = []
    pronouns = []

    proper_nouns = []
    normal_nouns = []
    modals = []
    adverbs = []
    adverbs_comp = []
    adverbs_sup = []
    adverbs_part = []
    base_verb = []
    verb_3 = []
    verb_n3 = []
    verb_past = []
    verb_pastp = []
    verb_gerund = []
    poss_pronoun = []

    for sent in tagged_sentences:
        for word, tags in sent:
            if tags.startswith('NN'):
                nouns.append(word)
            if tags == 'NNP' or tags == 'NNPS':
                proper_nouns.append(word)
            if tags == 'NN' or tags == 'NNS':
                normal_nouns.append(word)
            if tags.startswith("V") or tags.startswith("R") or tags.startswith("M"):
                verbs.append(word)
            if tags == 'MD':
                modals.append(word)
            if tags == 'RB':
                adverbs.append(word)
            if tags == 'RBR':
                adverbs_comp.append(word)
            if tags == 'RBS':
                adverbs_sup.append(word)
            if tags == 'RP':
                adverbs_part.append(word)
            if tags == 'VB':
                base_verb.append(word)
            if tags == 'VBZ':
                verb_3.append(word)
            if tags == 'VBP':
                verb_n3.append(word)
            if tags == 'VBD':
                verb_past.append(word)
            if tags == 'VBN':
                verb_pastp.append(word)
            if tags == 'VBG':
                verb_gerund.append(word)
            if tags.startswith('PRP'):
                pronouns.append(word)
            if tags == 'PRP$':
                poss_pronoun.append(word)
    all_len = [len(nouns), len(proper_nouns), len(verbs), len(modals), len(base_verb),
               len(adverbs), len(adverbs_comp), len(adverbs_part), len(adverbs_sup),
               len(verb_3), len(verb_n3), len(verb_gerund), len(verb_past), len(verb_pastp),
               len(pronouns), len(poss_pronoun)]

    ttr_proper_nouns = ttr_pos_entities(proper_nouns, nouns)
    ttr_modal_verbs = ttr_pos_entities(modals, verbs)
    ttr_base_verbs = ttr_pos_entities(base_verb, verbs)
    ttr_adverbs = ttr_pos_entities(adverbs, verbs)
    ttr_adverb_comp = ttr_pos_entities(adverbs_comp, verbs)
    ttr_adverb_sup = ttr_pos_entities(adverbs_sup, verbs)
    ttr_adverb_part = ttr_pos_entities(adverbs_part, verbs)
    ttr_verb_3 = ttr_pos_entities(verb_3, verbs)
    ttr_verb_n3 = ttr_pos_entities(verb_n3, verbs)
    ttr_verb_past = ttr_pos_entities(verb_past, verbs)
    ttr_verb_pastp = ttr_pos_entities(verb_pastp, verbs)
    ttr_verb_gerund = ttr_pos_entities(verb_gerund, verbs)
    ttr_possive_p = ttr_pos_entities(poss_pronoun, pronouns)
    scores = [0]

    if type(ttr_proper_nouns) == list:
        scores.extend(ttr_proper_nouns)
    else:
        scores.append(ttr_proper_nouns)

    if type(ttr_modal_verbs) == list:
        scores.extend(ttr_modal_verbs)
    else:
        scores.append(ttr_modal_verbs)

    if type(ttr_base_verbs) == list:
        scores.extend(ttr_base_verbs)
    else:
        scores.append(ttr_base_verbs)

    if type(ttr_adverbs) == list:
        scores.extend(ttr_adverbs)
    else:
        scores.append(ttr_adverbs)

    if type(ttr_adverb_comp) == list:
        scores.extend(ttr_adverb_comp)
    else:
        scores.append(ttr_adverb_comp)

    if type(ttr_adverb_sup) == list:
        scores.extend(ttr_adverb_sup)
    else:
        scores.append(ttr_adverb_sup)

    if type(ttr_adverb_part) == list:
        scores.extend(ttr_adverb_part)
    else:
        scores.append(ttr_adverb_part)

    if type(ttr_verb_3) == list:
        scores.extend(ttr_verb_3)
    else:
        scores.append(ttr_verb_3)

    if type(ttr_verb_n3) == list:
        scores.extend(ttr_verb_n3)
    else:
        scores.append(ttr_verb_n3)

    if type(ttr_verb_past) == list:
        scores.extend(ttr_verb_past)
    else:
        scores.append(ttr_verb_past)

    if type(ttr_verb_pastp) == list:
        scores.extend(ttr_verb_pastp)
    else:
        scores.append(ttr_verb_pastp)

    if type(ttr_verb_gerund) == list:
        scores.extend(ttr_verb_gerund)
    else:
        scores.append(ttr_verb_gerund)

    if type(ttr_possive_p) == list:
        scores.extend(ttr_possive_p)
    else:
        scores.append(ttr_possive_p)

    scores.remove(scores[0])

    return scores


def count_complex_tokens(sentences):
    sent_tokens_uncleaned = [tn.tokenize_text(sent) for sent in sentences]
    complex_tokens = [list(filter(lambda z: len(z) > 4, tokens)) for tokens in sent_tokens_uncleaned]
    return sum([len(n) for n in complex_tokens])


def count_stopwords(annotation):
    stopword_list = stopwords.words('english')
    stopword_count = 0
    for sentence in annotation['sentences']:
        stopword_count += len([token for token in sentence['tokens'] if token in stopword_list])
    return stopword_count


def extract_lexical_features(sentences, annotation):
    num_sentences = len(annotation['sentences'])
    num_tokens = sum(len(sentence['tokens']) for sentence in annotation['sentences'])
    num_stopwords = count_stopwords(annotation)

    # features
    complex_token_ratio = count_complex_tokens(sentences) / num_tokens
    number_meaningful_bigrams_percorpus = float(count_meaningful_bigrams(annotation)) / num_tokens
    stopword_ratio = num_stopwords / num_tokens
    stopword_per_sentence = num_stopwords / num_sentences

    # summarize features into an array
    scores = ttr_pos(annotation)
    scores.extend([
        complex_token_ratio,
        number_meaningful_bigrams_percorpus,
        stopword_ratio,
        stopword_per_sentence
    ])

    return scores


if __name__ == '__main__':
    cepp = DataSet('cepp')
    annotation = cepp.load_stanford_annotation(0)

    print(count_meaningful_bigrams(annotation))

    #test_data = """Eleven states working in conjunction with the U.S Department of Transportation (D.O.T) have agreed to implement an ordinance banning the use of electronic cigarettes in vehicles  meaning if you are a resident of one of the impacted states, you will be prohibited from utilizing an electronic cigarette while inside your vehicle."""
    #print(extract_lexical_features([test_data, test_data]))
    #print(list(find_ngrams(word_tokenize(test_data), 2)))
    #print(meanigful_bigrams(find_ngrams(word_tokenize(test_data), 2)))

