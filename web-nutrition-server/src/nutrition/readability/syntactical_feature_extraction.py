# -*- coding: utf-8 -*-
"""
Created on Sun Apr 08 07:04:22 2018

@author: simha

This program file extracts syntactical features using pattern, NLTK, and
Stanfordcore NLP libraries.

Stanford parsers must be downloaded and must be linked before parsing.
stanford-parser-3.5.2.jar and stanford-parser-3.5.2-models.jar must be downloaded.
http://book2s.com/java/jar/s/stanford-corenlp/download-stanford-corenlp-3.5.2.html
"""
from __future__ import division

import os

from nltk.parse.stanford import StanfordParser, StanfordDependencyParser
from nutrition.structure.environment import STANFORD_FOLDER
# from __future__ import division
## set java path
# import os
# java_path = r'C:\Program Files\Java\jdk-9.0.4\bin\java.exe'
# os.environ['JAVAHOME'] = java_path
#
# from nltk.parse.stanford import StanfordParser
# from nltk.parse.stanford import StanfordDependencyParser
#
#
# sdp = StanfordDependencyParser(path_to_jar='D:\stanford_parser_files/stanford-parser-3.5.2.jar',
#                     path_to_models_jar='D:\stanford_parser_files/stanford-parser-3.5.2-models.jar')
#
#
# result = sdp.raw_parse('I shot an elephant in my sleep')
##result = list(scp.raw_parse(sentence))
##dep_tree = [parse.tree() for parse in result][0]
##print dep_tree
#
from pattern.text.en import parsetree, Chunk
# from nltk.tree import Tree
#
# def clauses(sentence,scp):
#    result = list(scp.raw_parse(sentence))
#    count = 0
#    count1 = 0
#    temp_count = 0
#    dep_sents = []
#    indep_sents = []
#    for subtree in result[0].subtrees():
#        temp_count += 1
#        #if subtree.label()=="CC":
#            #print subtree
#        if subtree.label()=="S":
#            count1 +=1
#            indep_sents.append(' '.join(subtree.leaves()))
#
#        if subtree.label()=="SBAR":
#            count +=1
#            dep_sents.append(' '.join(subtree.leaves()))
#            #print ' '.join(subtree.leaves())
#    dep_sents = list(set(dep_sents))
#    indep_sents = list(set(indep_sents))
#    dependent_sentences = []
#    independent_sentences = [0]
#    for s in dep_sents:
#        temp = s.split(',')
#        dependent_sentences.append(temp[0])
#    #print dependent_sentences
##        dependent_sentences.append(s)
#
#    for s in indep_sents:
#        temp = s.split(',')
#        temp1 = [sent for sent in temp if sent not in dependent_sentences]
#        independent_sentences.extend(temp1)
#
#    independent_sentences.remove(0)
#
#    temp = dependent_sentences
#    dependent_sentences[:] = [sent.split(".")[0] for sent in dependent_sentences]
#    dependent_sentences[:] = [" ".join(sent.split()) for sent in dependent_sentences]
#
#
#    temp = independent_sentences
#    independent_sentences[:] = [sent.split(".")[0] for sent in independent_sentences]
#    independent_sentences[:] = [" ".join(sent.split()) for sent in independent_sentences]
#
#
#    #print independent_sentences
#    temp = [item for item in independent_sentences for w in dependent_sentences if item in w]
#    independent_sentences = [sent for sent in independent_sentences
#                                 if sent not in temp and sent not in dependent_sentences]
#
#    if not dependent_sentences:
#        if independent_sentences:
#            independent_sentences.remove(independent_sentences[0])
#
#    return [dependent_sentences,independent_sentences,temp]
#
#
## create a shallow parsed sentence tree
# def create_sentence_tree(sentence, lemmatize=False):
#    sentence_tree = parsetree(sentence,relations=True,
#                                lemmata=lemmatize) # if you want to lemmatize the tokens
#    return sentence_tree[0]
#
## get various constituents of the parse tree
# def get_sentence_tree_constituents(sentence_tree):
#    return sentence_tree.constituents()
#
## process the shallow parsed tree into an easy to understand format
# def process_sentence_tree(sentence_tree):
#    tree_constituents = get_sentence_tree_constituents(sentence_tree)
#    processed_tree = [(item.type,[(w.string, w.type) for w in item.words])
#                        if type(item) == Chunk else ('-',[(item.string, item.type)])
#                            for item in tree_constituents]
#    return processed_tree
#
## print the sentence tree using nltk's Tree syntax
# def print_sentence_tree(sentence_tree):
#    processed_tree = process_sentence_tree(sentence_tree)
#    processed_tree = [Tree( item[0],[Tree(x[1], [x[0]]) for x in item[1]])
#                        for item in processed_tree]
#    tree = Tree('S', processed_tree )
#    #print tree
#    return tree
#
## visualize the sentence tree using nltk's Tree syntax
# def visualize_sentence_tree(sentence_tree):
#    processed_tree = process_sentence_tree(sentence_tree)
#    processed_tree = [Tree( item[0],[Tree(x[1], [x[0]]) for x in item[1]])
#                        for item in processed_tree]
#    tree = Tree('S', processed_tree )
#    tree.draw()
#
# def syntacticalFeatureExtraction(sentences):
#    scp = StanfordParser(path_to_jar='D:\stanford_parser_files/stanford-parser-3.5.2.jar',
#                     path_to_models_jar='D:\stanford_parser_files/stanford-parser-3.5.2-models.jar')
#    num_noun_phrases = []
#    num_verb_phrases = []
#    num_adj_phrases = []
#    num_adv_phrases = []
#    num_prep_phrases = []
##    dependent_sents = []
##    independent_sents = []
##    noun_phrases_corpus = []
##    verb_phrases_corpus = []
##    adv_phrases_corpus = []
##    prep_phrases_corpus = []
#    tree_heights = []
#    num_subtrees = []
#
#    for s in sentences:
#
#        tree = parsetree(s)
#
#        # print all chunks
#
#        chunks = [sentence_tree.chunks for sentence_tree in tree]
#
#        noun_phrases_chunks = [chunk.words for chunk in chunks[0] if chunk.type=="NP"]
#        noun_phrases= [[(w.string,w.type) for w in word] for word in noun_phrases_chunks]
#
#        verb_phrases_chunks = [chunk.words for chunk in chunks[0] if chunk.type=="VP"]
#        verb_phrases= [[(w.string,w.type) for w in word] for word in verb_phrases_chunks]
#
#        adj_phrases_chunks = [chunk.words for chunk in chunks[0] if chunk.type=="ADJP"]
#        adj_phrases= [[(w.string,w.type) for w in word] for word in adj_phrases_chunks]
#
#        adverb_phrases_chunks = [chunk.words for chunk in chunks[0] if chunk.type=="ADVP"]
#        adverb_phrases= [[(w.string,w.type) for w in word] for word in adverb_phrases_chunks]
#
#        prep_phrases_chunks = [chunk.words for chunk in chunks[0] if chunk.type=="PP"]
#        prep_phrases= [[(w.string,w.type) for w in word] for word in prep_phrases_chunks]
#
#        # clauses
##        cl = clauses(s,scp)
##        dependent_sents.append(cl[0])
##        independent_sents.append(cl[1])
#
#        t = create_sentence_tree(s)
#        #pt = process_sentence_tree(t)
#        tr=print_sentence_tree(t)
#        #visualize_sentence_tree(t)
#        tree_heights.append(tr.height())
#        num_subtrees.append(len(list(tr.subtrees())))
#
#        num_noun_phrases.append(len(noun_phrases))
#        num_verb_phrases.append(len(verb_phrases))
#        num_adj_phrases.append(len(adj_phrases))
#        num_adv_phrases.append(len(adverb_phrases))
#        num_prep_phrases.append(len(prep_phrases))
#
#
##    num_dependent_clauses = [len(sent) for sent in dependent_sents]
##    num_independent_clauses = [len(sent) for sent in independent_sents]
#
#    tree_heights_per_corpus = float(sum(tree_heights))/len(tree_heights)
#    subtree_per_corpus = float(sum(num_subtrees))/len(num_subtrees)
#    noun_phrases_per_corpus = float(sum(num_noun_phrases))/len(num_noun_phrases)
#    verb_phrases_per_corpus = float(sum(num_verb_phrases))/len(num_verb_phrases)
#    adv_phrases_per_corpus = float(sum(num_adv_phrases))/len(num_adv_phrases)
#    adj_phrases_per_corpus = float(sum(num_adj_phrases))/len(num_adj_phrases)
#    prep_phrases_per_corpus = float(sum(num_prep_phrases))/len(num_adj_phrases)
##    dep_clauses_per_corpus = float(sum(num_dependent_clauses))/len(num_dependent_clauses)
##    indep_clauses_per_corpus = float(sum(num_independent_clauses))/len(num_independent_clauses)
##
##    return [tree_heights_per_corpus,subtree_per_corpus,noun_phrases_per_corpus,verb_phrases_per_corpus,
##            adv_phrases_per_corpus,adj_phrases_per_corpus,prep_phrases_per_corpus,
##            dep_clauses_per_corpus,indep_clauses_per_corpus]
#
#    return [tree_heights_per_corpus,subtree_per_corpus,noun_phrases_per_corpus,verb_phrases_per_corpus,
#            adv_phrases_per_corpus,adj_phrases_per_corpus,prep_phrases_per_corpus]
#
##sentence2 = "Though he was very rich, he was still very unhappy."


# set java path
# import os
# java_path = r'C:\Program Files\Java\jdk-9.0.4\bin\java.exe'
# os.environ['JAVAHOME'] = java_path

# from nltk.parse.stanford import StanfordParser
# from nltk.parse.stanford import StanfordDependencyParser


# sdp = StanfordDependencyParser(path_to_jar='D:\stanford_parser_files/stanford-parser-3.5.2.jar',
#                      path_to_models_jar='D:\stanford_parser_files/stanford-parser-3.5.2-models.jar')


# result = sdp.raw_parse('I shot an elephant in my sleep')
# result = list(scp.raw_parse(sentence))
# dep_tree = [parse.tree() for parse in result][0]
# print dep_tree

# from pattern.en import parsetree, Chunk
from nltk.tree import Tree


# calculate dependency parse tree height
def calculate_dependencies(sentences, sdp):
    x = sdp.raw_parse_sents(sentences)
    dep_tree = [[parse.tree() for parse in list(sent)] for sent in x]
    depth = [tree[0].height() for tree in dep_tree]
    return depth


# def clauses(sentence,scp):
#    result = list(scp.raw_parse(sentence))
#    count = 0
#    count1 = 0
#    temp_count = 0
#    dep_sents = []
##    indep_sents = []
#    for subtree in result[0].subtrees():
#        temp_count += 1
#        #if subtree.label()=="CC":
#            #print subtree
##         if subtree.label()=="S":
##             count1 +=1
##             indep_sents.append(' '.join(subtree.leaves()))
#
#        if subtree.label()=="SBAR":
#            count +=1
#            dep_sents.append(' '.join(subtree.leaves()))
#            #print ' '.join(subtree.leaves())
#    dep_sents = list(set(dep_sents))
##     indep_sents = list(set(indep_sents))
#    dependent_sentences = []
##     independent_sentences = [0]
#    for s in dep_sents:
#        temp = s.split(',')
#        dependent_sentences.append(temp[0])
#    #print dependent_sentences
##        dependent_sentences.append(s)
#
##     for s in indep_sents:
##         temp = s.split(',')
##         temp1 = [sent for sent in temp if sent not in dependent_sentences]
##         independent_sentences.extend(temp1)
#
##     independent_sentences.remove(0)
#
#    temp = dependent_sentences
#    dependent_sentences[:] = [sent.split(".")[0] for sent in dependent_sentences]
#    dependent_sentences[:] = [" ".join(sent.split()) for sent in dependent_sentences]
#
#
##     temp = independent_sentences
##     independent_sentences[:] = [sent.split(".")[0] for sent in independent_sentences]
##     independent_sentences[:] = [" ".join(sent.split()) for sent in independent_sentences]
#
#
##     #print independent_sentences
##     temp = [item for item in independent_sentences for w in dependent_sentences if item in w]
##     independent_sentences = [sent for sent in independent_sentences
##                                  if sent not in temp and sent not in dependent_sentences]
#
##     if not dependent_sentences:
##         if independent_sentences:
##             independent_sentences.remove(independent_sentences[0])
#
##     return [dependent_sentences,independent_sentences,temp]
#    return dependent_sentences

# Extract number of dependent sentences per article
def clauses(sentences, scp):
    y = scp.raw_parse_sents(sentences)
    z = list(y)
    z1 = [list(x) for x in z]
    deps = []
    for sent in z1:
        for subtree in sent[0].subtrees():
            if subtree.label() == "SBAR":
                # count +=1
                deps.append(' '.join(subtree.leaves()))

    dep_sents = list(set(deps))
    #     indep_sents = list(set(indep_sents))
    dependent_sentences = []
    #     independent_sentences = [0]
    for s in dep_sents:
        temp = s.split(',')
        dependent_sentences.append(temp[0])
    # print dependent_sentences
    #        dependent_sentences.append(s)

    #     for s in indep_sents:
    #         temp = s.split(',')
    #         temp1 = [sent for sent in temp if sent not in dependent_sentences]
    #         independent_sentences.extend(temp1)

    #     independent_sentences.remove(0)

    temp = dependent_sentences
    dependent_sentences[:] = [sent.split(".")[0] for sent in dependent_sentences]
    dependent_sentences[:] = [" ".join(sent.split()) for sent in dependent_sentences]
    return dependent_sentences


# create a shallow parsed sentence tree
def create_sentence_tree(sentence, lemmatize=False):
    sentence_tree = parsetree(sentence, relations=True,
                              lemmata=lemmatize)  # if you want to lemmatize the tokens
    return sentence_tree[0]


# get various constituents of the parse tree
def get_sentence_tree_constituents(sentence_tree):
    return sentence_tree.constituents()


# process the shallow parsed tree into an easy to understand format
def process_sentence_tree(sentence_tree):
    tree_constituents = get_sentence_tree_constituents(sentence_tree)
    processed_tree = [(item.type, [(w.string, w.type) for w in item.words])
                      if type(item) == Chunk else ('-', [(item.string, item.type)])
                      for item in tree_constituents]
    return processed_tree


# print the sentence tree using nltk's Tree syntax
def print_sentence_tree(sentence_tree):
    processed_tree = process_sentence_tree(sentence_tree)
    processed_tree = [Tree(item[0], [Tree(x[1], [x[0]]) for x in item[1]])
                      for item in processed_tree]
    tree = Tree('S', processed_tree)
    # print tree
    return tree


# visualize the sentence tree using nltk's Tree syntax
def visualize_sentence_tree(sentence_tree):
    processed_tree = process_sentence_tree(sentence_tree)
    processed_tree = [Tree(item[0], [Tree(x[1], [x[0]]) for x in item[1]])
                      for item in processed_tree]
    tree = Tree('S', processed_tree)
    tree.draw()


# Extract different phrases from a sentence: different phrases can be extracted
# using pattern API.
def extract_syntactical_features(sentences, scp, sdp):
    #     scp = StanfordParser(path_to_jar='D:\stanford_parser_files/stanford-parser-3.5.2.jar',
    #                      path_to_models_jar='D:\stanford_parser_files/stanford-parser-3.5.2-models.jar')
    num_noun_phrases = []
    num_verb_phrases = []
    num_adj_phrases = []
    num_adv_phrases = []
    num_prep_phrases = []
    # dependent_sents = []
    #    independent_sents = []
    #    noun_phrases_corpus = []
    #    verb_phrases_corpus = []
    #    adv_phrases_corpus = []
    #    prep_phrases_corpus = []
    tree_heights = calculate_dependencies(sentences, sdp)
    cl = clauses(sentences, scp)
    dependent_sents = cl
    #     num_subtrees = []

    for s in sentences:
        tree = parsetree(s)

        # print all chunks

        chunks = [sentence_tree.chunks for sentence_tree in tree]

        noun_phrases_chunks = [chunk.words for chunk in chunks[0] if chunk.type == "NP"]
        noun_phrases = [[(w.string, w.type) for w in word] for word in noun_phrases_chunks]

        verb_phrases_chunks = [chunk.words for chunk in chunks[0] if chunk.type == "VP"]
        verb_phrases = [[(w.string, w.type) for w in word] for word in verb_phrases_chunks]

        adj_phrases_chunks = [chunk.words for chunk in chunks[0] if chunk.type == "ADJP"]
        adj_phrases = [[(w.string, w.type) for w in word] for word in adj_phrases_chunks]

        adverb_phrases_chunks = [chunk.words for chunk in chunks[0] if chunk.type == "ADVP"]
        adverb_phrases = [[(w.string, w.type) for w in word] for word in adverb_phrases_chunks]

        prep_phrases_chunks = [chunk.words for chunk in chunks[0] if chunk.type == "PP"]
        prep_phrases = [[(w.string, w.type) for w in word] for word in prep_phrases_chunks]

        # clauses

        #        independent_sents.append(cl[1])

        #         t = create_sentence_tree(s)
        #         #pt = process_sentence_tree(t)
        #         tr=print_sentence_tree(t)
        #         #visualize_sentence_tree(t)
        #         tree_heights.append(tr.height())
        #         num_subtrees.append(len(list(tr.subtrees())))
        # tree_heights.append(calculate_dependencies(s,sdp))

        num_noun_phrases.append(len(noun_phrases))
        num_verb_phrases.append(len(verb_phrases))
        num_adj_phrases.append(len(adj_phrases))
        num_adv_phrases.append(len(adverb_phrases))
        num_prep_phrases.append(len(prep_phrases))

    # num_dependent_clauses = [len(sent) for sent in dependent_sents]
    #    num_independent_clauses = [len(sent) for sent in independent_sents]

    tree_heights_per_corpus = float(sum(tree_heights)) / len(tree_heights)
    # subtree_per_corpus = float(sum(num_subtrees))/len(num_subtrees)
    noun_phrases_per_corpus = float(sum(num_noun_phrases)) / len(num_noun_phrases)
    verb_phrases_per_corpus = float(sum(num_verb_phrases)) / len(num_verb_phrases)
    adv_phrases_per_corpus = float(sum(num_adv_phrases)) / len(num_adv_phrases)
    adj_phrases_per_corpus = float(sum(num_adj_phrases)) / len(num_adj_phrases)
    prep_phrases_per_corpus = float(sum(num_prep_phrases)) / len(num_adj_phrases)
    #    dep_clauses_per_corpus = float(sum(num_dependent_clauses))/len(num_dependent_clauses)
    dep_clauses_per_corpus = float(len(dependent_sents)) / len(sentences)
    #    indep_clauses_per_corpus = float(sum(num_independent_clauses))/len(num_independent_clauses)
    #
    #    return [tree_heights_per_corpus,subtree_per_corpus,noun_phrases_per_corpus,verb_phrases_per_corpus,
    #            adv_phrases_per_corpus,adj_phrases_per_corpus,prep_phrases_per_corpus,
    #            dep_clauses_per_corpus,indep_clauses_per_corpus]

    return [tree_heights_per_corpus, noun_phrases_per_corpus, verb_phrases_per_corpus,
            adv_phrases_per_corpus, adj_phrases_per_corpus, prep_phrases_per_corpus, dep_clauses_per_corpus]

# sentence2 = "Though he was very rich, he was still very unhappy."



if __name__ == '__main__':
    java_path = r'C:/Program Files/Java/jre1.8.0_171'
    os.environ['JAVAHOME'] = java_path

    scp = StanfordParser(
        path_to_jar=STANFORD_FOLDER + '/stanford-corenlp-3.9.1.jar',
        path_to_models_jar=STANFORD_FOLDER + '/stanford-corenlp-3.9.1-models.jar')

    sdp = StanfordDependencyParser(
        path_to_jar=STANFORD_FOLDER + '/stanford-corenlp-3.9.1.jar',
        path_to_models_jar=STANFORD_FOLDER + '/stanford-corenlp-3.9.1-models.jar')

    test_data = """Eleven states working in conjunction with the U.S Department of Transportation (D.O.T) have agreed to implement an ordinance banning the use of electronic cigarettes in vehicles  meaning if you are a resident of one of the impacted states, you will be prohibited from utilizing an electronic cigarette while inside your vehicle."""
    print(extract_syntactical_features([test_data], scp, sdp))
