'''
This script is for extracting features from a stanford parse tree.
'''
import pickle

from nltk.tree import Tree
from nltk.stem.snowball import SnowballStemmer
import pprint

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
# TODO: should we ignore punctuations, special characters? Refine the filter.
def count_types(sentence_trees):
    stemmer = SnowballStemmer('english')
    
    stem_counts = {}
    
    for tree in sentence_trees:
        for pos in tree.treepositions():
            node = tree[pos]
            if type(node) is str:
                if True in [c in node.lower() for c in 'abcdefghijklmnopqrstuvwxyz']:
                    stem = stemmer.stem(node)
                    if stem in stem_counts.keys():
                        stem_counts[stem] += 1
                    else:
                        stem_counts[stem] = 1
    
    type_count = len(stem_counts)
    token_count = sum(stem_counts.values())
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
    type_count, token_count = count_types(sentence_trees)
    
    return [
        # ------------- phrase tags -------------
        # number of NPs per sentence
        get_sum(non_terminal_count, ['NP', 'NX']) / num_sentences,
        
        # number of VPs per sentence
        get_sum(non_terminal_count, ['VP']) / num_sentences,
        
        
        # -------------- word tags --------------
        # ratio of pronouns
        get_sum(terminal_count, ['PRP', 'PRP$', 'WP', 'WP$']) / num_sentences,       # possessive pronouns
        
        # preposition token per sentence
        get_sum(terminal_count, ['NN', 'NNS', 'NNP', 'NNPS']) / num_sentences,       # nouns
        
        # noun token per sentence        
        get_sum(terminal_count, ['IN']) / num_sentences,                             # preposition
        
        
        # --------------- others ----------------
        # number of non-terminal nodes per parse tree
        count_non_terminal_nodes(sentence_trees) / num_sentences,
        
        # type-token ratio
        type_count / token_count,
        
        # tokens per sentence
        token_count/ num_sentences
        
    ]

if __name__ == '__main__':
    with open('D:/master project/data/newsela/standford_annotate/' + str(1), 'rb') as file:
        annotation = pickle.load(file)
    
    print(get_features(annotation))
    