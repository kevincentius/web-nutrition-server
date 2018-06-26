# -*- coding: utf-8 -*-
"""
Created on Thu Apr 05 15:02:47 2018

@author: simha
"""

import nltk
import re,collections
import string
from pprint import pprint
from contractions import contractions_dict
from nltk.corpus import wordnet as wn
from pattern3.text.en import tag
#corpus = "The brown fox wasn't that quick and he couldn't win the race. Hey that's a great deal!, I just bought a phone for $199. @@You'll (learn) a **lot** in the book. Python is an amazing language!,@@."

# word Tokenization
def tokenize_text(text):
    sents = nltk.sent_tokenize(text)
    if len(sents)>1:
        #tokens = []
        temp1 = [nltk.word_tokenize(sent) for sent in sents]
        tokens = [[token.strip() for token in words] for words in temp1]
    else:
        tokens = nltk.word_tokenize(text)
        tokens = [token.strip() for token in tokens]
               
    return tokens


# Remove symbols from the text like currency symbols
    
def remove_characters_before_tokenization(sentence,keep_apostrophes=False):
    sentence = sentence.strip()
    if keep_apostrophes:
        PATTERN = r'[?|$|&|*|%|@|(|)|~|,]' # add other characters here toremove them
        filtered_sentence = re.sub(PATTERN, r'', sentence)
    else:
        PATTERN = r'[^a-zA-Z0-9 ]' # only extract alpha-numeric characters
        filtered_sentence = re.sub(PATTERN, r'', sentence)
    return filtered_sentence

#cleaned_corpus = [remove_characters_before_tokenization(sentence,
#                        keep_apostrophes=True) for sentence in x[1]]

# Expanding COntractions

def expand_contractions(sentence, contraction_mapping=contractions_dict):
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())),
                                      flags=re.IGNORECASE|re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match)\
        if contraction_mapping.get(match)\
        else contraction_mapping.get(match.lower())
        expanded_contraction = first_char+expanded_contraction[1:]
        return expanded_contraction
    expanded_sentence = contractions_pattern.sub(expand_match, sentence)
    return expanded_sentence

# Remove stopwrds

#def remove_stopwords(tokens):
#    stopword_list = nltk.corpus.stopwords.words('english')
#    filtered_tokens = [token for token in tokens if token not in stopword_list]
#    return filtered_tokens

#expanded_corpus_tokens = [tokenize_text(text) for text in expanded_corpus]
    
# Remove repeated characters if any. like realllyyy....

def remove_repeated_characters(tokens):
    repeat_pattern = re.compile(r'(\w*)(\w)\2(\w*)')
    match_substitution = r'\1\2\3'
    
    def replace(old_word):
        if wn.synsets(old_word):
            return old_word
        new_word = repeat_pattern.sub(match_substitution, old_word)
        return replace(new_word) if new_word != old_word else new_word
    
    correct_tokens = [replace(word) for word in tokens]
    return correct_tokens    

# Lemmatization
def pos_tag_text(text):
    def penn_to_wn_tags(pos_tag):
        if pos_tag.startswith('J'):
            return wn.ADJ
        elif pos_tag.startswith('V'):
            return wn.VERB
        elif pos_tag.startswith('N'):
            return wn.NOUN
        elif pos_tag.startswith('R'):
            return wn.ADV
        else:
            return None
    if type(text)==list:
        tagged_text = [tag(t) for t in text]
        tagged_lower_text = [[(word.lower(), penn_to_wn_tags(pos_tag))
                                for word, pos_tag in t] for t in tagged_text]
    else:       
        tagged_text = tag(text)
        tagged_lower_text = [(word.lower(), penn_to_wn_tags(pos_tag))
                                for word, pos_tag in tagged_text]
    return tagged_lower_text

def lemmatize_text(text):
    pos_tagged_text = pos_tag_text(text)
    
    if type(text)==list:
       lemmatized_tokens = [[wn.lemmatize(word, pos_tag) if pos_tag
                             else word for word, pos_tag in t] for t in pos_tagged_text]
       lemmatized_text = [' '.join(tok) for tok in lemmatized_tokens] 
    else:
        lemmatized_tokens = [wn.lemmatize(word, pos_tag) if pos_tag
                             else word for word, pos_tag in pos_tagged_text]
        lemmatized_text = ' '.join(lemmatized_tokens)
    
    
    return lemmatized_text


# remove symbols
def remove_special_characters(text):
    tokens = tokenize_text(text)
    pattern = re.compile('[{}]'.format(re.escape(string.punctuation)))
    filtered_tokens = filter(None, [pattern.sub('', token) for token in
    tokens])
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text

# remove stopwords
#def remove_stopwords(text):
#    tokens = tokenize_text(text)
#    filtered_tokens = [token for token in tokens if token not in stopword_list]
#    filtered_text = ' '.join(filtered_tokens)
#    return filtered_text
    
# Normalize Corpus
#def normalize_corpus(corpus, tokenize=False):
#    normalized_corpus = []
#    for text in corpus:
#        text = expand_contractions(text, contractions_dict)
#        text = lemmatize_text(text)
#        text = remove_special_characters(text)
#        text = remove_stopwords(text)
#        normalized_corpus.append(text)
#        if tokenize:
#            text = tokenize_text(text)
#            normalized_corpus.append(text)
#    return normalized_corpus