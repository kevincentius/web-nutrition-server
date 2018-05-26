'''
This script is for extracting features from a stanford parse tree.
'''
import pickle

from nltk.tree import Tree
import sys

def count_tags(sentence_trees):
    terminal_count = {}
    non_terminal_count = {}
    
    
    for tree in sentence_trees:
        for pos in tree.treepositions():
            node = tree[pos]
            if type(node) is str:
                # ignore leave node, which is a word/token (string)
                continue
            
            label = node.label().split('-')[0]
            
            if type(node[0]) is str:
                # label of leave node (single word label)
                if label in terminal_count:
                    terminal_count[label] += 1
                else:
                    terminal_count[label] = 1
            else:
                # subtree (phrase label)
                if label in non_terminal_count:
                    non_terminal_count[label] += 1
                else:
                    non_terminal_count[label] = 1
                    
    return terminal_count, non_terminal_count

# 'Type VS Token' count
# Tokens that contains no letter is ignored.
def count_types(annotation):
    lemma_counts = {}
    
    for sentence in annotation['sentences']:
        for token in sentence['tokens']:
            # ignore tokens that has no letter in it (e.g. punctuations, numbers)
            if not True in [c in  token['word'].lower() for c in 'abcdefghijklmnopqrstuvwxyz']:
                continue
            
            lemma = token['lemma']
            if lemma in lemma_counts:
                lemma_counts[lemma] += 1
            else:
                lemma_counts[lemma] = 1
            
    type_count = len(lemma_counts)
    token_count = sum(lemma_counts.values())
    return type_count, token_count

# returns null safe sum of counts of tags listed as `labels`
def get_sum(count_map, labels):
    count = 0
    for label in labels:
        if label in count_map.keys():
            count += count_map[label]
    return count

# returns false if the node is a string (word itself) or a POS tag of a single word/token
# returns true if the node is a phrase level node, which means it contains child nodes
def is_node_phrase_level(child):
    return type(child) is not str and type(child[0]) is not str

# returns the number of non terminal nodes (phrase level)
def count_non_terminal_nodes(sentence_trees):
    count = 0
    for tree in sentence_trees:
        for pos in tree.treepositions():
            node = tree[pos]
            
            # ignore word level nodes
            if is_node_phrase_level(node):
                
                # if at least one of the node's children is a phrase level node,
                #    that means the node is non terminal
                #    -> count it
                for child in node:
                    if is_node_phrase_level(child):
                        count += 1
                        break

    return count

def get_features(annotation):
    num_sentences = len(annotation['sentences'])
    sentence_trees = [Tree.fromstring(sentence['parse']) for sentence in annotation['sentences']]
    terminal_count, non_terminal_count = count_tags(sentence_trees)
    type_count, token_count = count_types(annotation)
    
    phrase_tags = ['ADJP', 'ADVP', 'CONJP', 'FRAG', 'INTJ', 'LST', 'NAC', 'NP', 'NX', 'PP', 'PRN', 'PRT', 'QP', 'RRC', 'UCP', 'VP', 'WHADJP', 'WHAVP', 'WHNP', 'WHPP', 'X']
    word_tags = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB']
    
    features = []
    
    for phrase_tag in phrase_tags:
        features.append(get_sum(non_terminal_count, [phrase_tag]) / token_count)
        features.append(get_sum(non_terminal_count, [phrase_tag]) / num_sentences)
    
    for word_tag in word_tags:
        features.append(get_sum(terminal_count, [word_tag]) / token_count)
        features.append(get_sum(terminal_count, [word_tag]) / num_sentences)
    
    features.extend([
        # --------------- others ----------------
        # number of non-terminal nodes per parse tree
        count_non_terminal_nodes(sentence_trees) / num_sentences,
        
        # type-token ratio
        type_count / token_count,
        
        # tokens per sentence
        token_count / num_sentences
    ])
    
    return features

if __name__ == '__main__':
    with open('D:/git/web-nutrition-server/web-nutrition-server/src/data/cepp/stanford/0', 'rb') as file:
        annotation = pickle.load(file)
    
    #pprint.pprint(annotation)
    #sentence_trees = [Tree.fromstring(sentence['parse']) for sentence in annotation['sentences']]
    #sentence_trees[0].pretty_print()
    for sentence in annotation['sentences']:
        for token in sentence['tokens']:
            print(token['lemma'], token['word'], token['originalText'], token['pos'])
    
    print(count_types(annotation))    
    
    #sys.exit()
    
    print(get_features(annotation))
    