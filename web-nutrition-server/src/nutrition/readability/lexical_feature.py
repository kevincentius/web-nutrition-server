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

from pattern.text.en import tag
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import word_tokenize
from nltk import FreqDist
from contractions import fix


# txt = """Natural language processing (NLP) is a field of computer science, artificial intelligence, and computational linguistics concerned with the inter
# actions between computers and human (natural) languages."""


# sentence = "The brown fox wasn't that quick and he couldn't win the race."

# finding ngrams
from nutrition.readability import text_normalization as tn


def find_ngrams(input_list, n):
    return zip(*[input_list[i:] for i in range(n)])


# Extracting meaningful bigrams like United States Jon peter....
def meanigful_bigrams(bgram):
    bigrams = []

    # for j in bgram:
    #     tag1 = tag(j[0])[0][1]
    #     tag2 = tag(j[1])[0][1]
    #
    #     if tag1 in ['NNP', 'NN', 'JJ'] and tag2 in ['NNP', 'NN']:
    #         bigrams.append(' '.join(j))

    return bigrams


# word complexity
def word_complexity(tokens):
    complex_words = filter(lambda z: len(z) > 4, tokens)


#    meaningful_bigrams = []
# complex_words.append()

# Extract difficult words based on length and frequency
def difficult_words(word_tokens):
    difficult_words_article = []
    word_tokens_flat = [word for sent in word_tokens for word in sent]
    #    for sent in word_tokens:
    #        for word in sent:
    #            word_tokens_flat.extend(word)
    #    word_tokens_flat.remove(word_tokens_flat[0])
    #    word_tokens_flat = [word for tok in word_tokens for word in tok]
    word_freq = FreqDist(word_tokens_flat)
    all_words = word_freq.keys()

    for word in all_words:
        if word_freq[word] <= 2 and len(word) >= 4:
            difficult_words_article.append(word)
    #    print('---------difficult-----')
    #    print(difficult_words_article)
    return difficult_words_article


# different type token ratios
def ttr(corpus):
    vectorizer = CountVectorizer()
    vectorizer.fit_transform(corpus)
    unique_words = vectorizer.get_feature_names()
    words = [0]
    [words.extend(word_tokenize(s)) for s in corpus]
    words.remove(words[0])
    n = len(words)
    t = len(unique_words)

    # normal type token ratio
    nttr = float(t) / n

    # root type token ratio
    rttr = float(t) / (n ** 0.5)

    # corrected type token ratio
    cttr = float(t) / ((2 * n) ** 0.5)

    # mass type token ratio
    f = lambda x, y: [x[i:i + y] for i in range(0, len(x), y)]
    x = f(words, 100)
    y = [(FreqDist(sect), len(sect)) for sect in x]
    z = [float(len(sect[0].keys())) / sect[1] for sect in y]

    msttr = sum(z) / len(z)

    if n > 0 and t > 0:
        mass = (math.log(n) - math.log(t)) / math.log(n) ** 2
        return [nttr, rttr, cttr, mass, msttr]
    else:
        return [nttr, rttr, cttr, 0.0, msttr]


# type token ratios calcuations
def ttr_pos_entities(pos_words, all_words):
    n = len(all_words)
    t = len(pos_words)
    if n > 0 and t > 0:
        nttr = float(t) / n
        rttr = float(t) / (n ** 0.5)
        cttr = float(t) / ((2 * n) ** 0.5)
        mass = (math.log(n) - math.log(t)) / math.log(n) ** 2
        return [nttr, rttr, cttr, mass]
    else:
        return [0, 0, 0, 0]


# type token ratios for different POS tags
def ttr_pos(corpus_tagged):
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

    for sent in corpus_tagged:
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


# lexical features
def extract_lexical_features(sentences):
    #    sentences = corpus_sents
    stopword_list = stopwords.words('english')

    # expand isn't to is not etc..
    cleaned_sentences = [fix(sentence) for sentence in sentences]
    #    cleaned_sentences = [tn.expand_contractions(sentence) for sentence in sentences]
    # pos tagging the sentences

    tagged_sentences = [tag(cleaned_sent) for cleaned_sent in cleaned_sentences]
    cleaned_sent_tokens = [word_tokenize(cleaned_sent) for cleaned_sent in cleaned_sentences]
    #print('------cleaned_sent_tokens------')
    #print(cleaned_sent_tokens)

    # remove stop words
    cleaned_sent_stop_words_removed = [cleaned_sent_tokens
                                       for cleaned_sent_token in cleaned_sent_tokens
                                       if cleaned_sent_token not in stopword_list]
    # sentence tokenization
    sent_tokens_uncleaned = [tn.tokenize_text(sent) for sent in sentences]

    # extract long tokens of lenght more than 4
    complex_tokens = [list(filter(lambda z: len(z) > 4, tokens)) for tokens in sent_tokens_uncleaned]

    # extract bigrams
    Bigrams = [find_ngrams(wordlist, 2) for wordlist in cleaned_sent_tokens]
    # print(len(Bigrams))

    # extract meaning ful bigrams like United States Jon peter....
    wanted_bigrams = [meanigful_bigrams(bg) for bg in Bigrams]
    wanted_bigrams = filter(None, wanted_bigrams)
    wanted_bigrams = [bg for gram in wanted_bigrams for bg in gram]

    #    stopword_list = [word for word in stopword_list if word not in determiner_tokens]
    #    function_words = [word for word in cleaned_sent_tokens if word in stopword_list]
    #    function_words = set(function_words)
    # various pos tokens
    nouns_tokens = []
    verb_all_tokens = []
    adverb_tokens = []
    modal_tokens = []
    verb_tokens = []
    determiner_tokens = []
    pronoun_tokens = []
    predet_tokens = []
    adjective_tokens = []
    Foriegn_tokens = []
    function_words = []

    for sent in sentences:
        temp = [words for words in sent if words in stopword_list]
        function_words.append(temp)

    # pos tagging
    for sent in tagged_sentences:
        temp_noun = []
        temp_verb_all = []
        temp_adverb = []
        temp_modal = []
        temp_verb = []
        temp_det = []
        temp_pron = []
        temp_predet = []
        temp_adj = []
        temp_foriegn = []

        for word, tags in sent:
            # Nouns
            if tags.startswith("NN"):
                if word not in nouns_tokens:
                    temp_noun.append(word)
            # all verbs
            if tags.startswith("V") or tags.startswith("R") or tags.startswith("M"):
                if word not in verb_all_tokens:
                    temp_verb_all.append(word)
            # adverbs
            if tags.startswith("R"):
                if word not in adverb_tokens:
                    temp_adverb.append(word)
            # Modal verbs
            if tags.startswith("M"):
                if word not in modal_tokens:
                    temp_modal.append(word)
            # verbs
            if tags.startswith("V"):
                if word not in verb_tokens:
                    temp_verb.append(word)
            # determiners
            if tags.startswith("D"):
                if word not in determiner_tokens:
                    temp_det.append(word)
            # pronouns
            if tags.startswith("PRP"):
                if word not in pronoun_tokens:
                    temp_pron.append(word)
            # predeterminers
            if tags.startswith("PDT"):
                if word not in predet_tokens:
                    temp_predet.append(word)
            # adjectives
            if tags.startswith("J"):
                if word not in adjective_tokens:
                    temp_adj.append(word)
            # Foriegn Tokens
            if tags.startswith("F"):
                if word not in Foriegn_tokens:
                    temp_foriegn.append(word)

        nouns_tokens.append(temp_noun)

        verb_all_tokens.append(temp_verb_all)

        adverb_tokens.append(temp_adverb)

        modal_tokens.append(temp_modal)

        verb_tokens.append(temp_verb)

        determiner_tokens.append(temp_det)

        pronoun_tokens.append(temp_pron)

        predet_tokens.append(temp_predet)

        adjective_tokens.append(temp_adj)

        Foriegn_tokens.append(temp_foriegn)

    number_of_tokens_per_corpus = sum([len(tok) for tok in cleaned_sent_tokens])

    complex_tokens_len = [len(n) for n in complex_tokens]
    complex_tokens_per_sent = [float(complex_tokens_len[i]) / len(sent_tokens_uncleaned[i])
                               for i in range(len(sentences))]

    number_tokens = []
    for i in range(len(sentences)):
        temp = float(len(cleaned_sent_stop_words_removed[i])) / len(sent_tokens_uncleaned[i])
        number_tokens.append(temp)

    nouns_len = [len(n) for n in nouns_tokens]
    nouns_per_sent = []
    for i in range(len(sentences)):
        nouns_per_sent.append(float(nouns_len[i]) / len(sent_tokens_uncleaned[i]))

    verbs_all_len = [len(n) for n in verb_all_tokens]
    verbs_all_per_sent = [float(verbs_all_len[i]) / len(sent_tokens_uncleaned[i])
                          for i in range(len(sentences))]

    adverb_len = [len(n) for n in adverb_tokens]
    adverbs_per_sent = [float(adverb_len[i]) / len(sent_tokens_uncleaned[i])
                        for i in range(len(sentences))]

    modal_len = [len(n) for n in modal_tokens]
    modals_per_sent = [float(modal_len[i]) / len(sent_tokens_uncleaned[i])
                       for i in range(len(sentences))]

    verbs_len = [len(n) for n in verb_tokens]
    verbs_per_sent = [float(verbs_len[i]) / len(sent_tokens_uncleaned[i])
                      for i in range(len(sentences))]

    det_len = [len(n) for n in determiner_tokens]
    det_per_sent = [float(det_len[i]) / len(sent_tokens_uncleaned[i])
                    for i in range(len(sentences))]

    pronoun_len = [len(n) for n in pronoun_tokens]
    pronoun_per_sent = [float(pronoun_len[i]) / len(sent_tokens_uncleaned[i])
                        for i in range(len(sentences))]

    predet_len = [len(n) for n in predet_tokens]
    predet_per_sent = [float(predet_len[i]) / len(sent_tokens_uncleaned[i])
                       for i in range(len(sentences))]

    adj_len = [len(n) for n in adjective_tokens]
    adj_per_sent = [float(adj_len[i]) / len(sent_tokens_uncleaned[i])
                    for i in range(len(sentences))]

    foriegn_len = [len(n) for n in Foriegn_tokens]
    foriegn_per_sent = [float(foriegn_len[i]) / len(sent_tokens_uncleaned[i])
                        for i in range(len(sentences))]

    function_words_len = [len(n) for n in function_words]
    function_words_per_sent = [float(function_words_len[i]) / len(sent_tokens_uncleaned[i])
                               for i in range(len(sentences))]

    # caalculating arious tokens per article
    complex_tokens_per_corpus = sum(complex_tokens_per_sent) / len(sentences)
    num_token_corpus = sum(number_tokens) / len(sentences)
    nouns_per_corpus = sum(nouns_per_sent) / len(sentences)
    verbs_all_per_corpus = sum(verbs_all_per_sent) / len(sentences)
    adverbs_per_corpus = sum(adverbs_per_sent) / len(sentences)
    modals_per_corpus = sum(modals_per_sent) / len(sentences)
    verbs_per_corpus = sum(verbs_per_sent) / len(sentences)
    det_per_corpus = sum(det_per_sent) / len(sentences)
    pronouns_per_corpus = sum(pronoun_per_sent) / len(sentences)
    adj_per_corpus = sum(adj_per_sent) / len(sentences)
    foriegn_per_corpus = sum(foriegn_per_sent) / len(sentences)
    function_words_per_corpus = sum(function_words_per_sent) / len(sentences)

    ttr_corpus = ttr(sentences)
    ttr_corpus_tagged = ttr_pos(tagged_sentences)
    ttr_corpus.extend(ttr_corpus_tagged)

    difficult_words_article = difficult_words(cleaned_sent_tokens)

    number_meaningful_bigrams_percorpus = float(len(wanted_bigrams)) / number_of_tokens_per_corpus
    difficult_words_per_article = float(len(difficult_words_article)) / number_of_tokens_per_corpus

    scores = [num_token_corpus, nouns_per_corpus, verbs_all_per_corpus,
              adverbs_per_corpus, modals_per_corpus, verbs_per_corpus, det_per_corpus,
              pronouns_per_corpus, adj_per_corpus, complex_tokens_per_corpus,
              function_words_per_corpus, number_meaningful_bigrams_percorpus, difficult_words_per_article]
    ttr_corpus.extend(scores)

    return ttr_corpus


if __name__ == '__main__':
    test_data = """Eleven states working in conjunction with the U.S Department of Transportation (D.O.T) have agreed to implement an ordinance banning the use of electronic cigarettes in vehicles  meaning if you are a resident of one of the impacted states, you will be prohibited from utilizing an electronic cigarette while inside your vehicle."""
    print(extract_lexical_features([test_data, test_data]))
