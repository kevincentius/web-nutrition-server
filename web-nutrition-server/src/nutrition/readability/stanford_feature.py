'''
This script is for extracting features from a stanford parse tree.
'''
import math
import numpy as np
from nltk.tree import Tree

from nutrition.structure.data_set import DataSet


def count_sum_node_depth(sentence_trees):
    total = 0
    for tree in sentence_trees:
        for pos in tree.treepositions():
            node = tree[pos]
            if type(node) is str:
                total += len(pos)

    return total


def count_sum_word_length(sentence_trees):
    total = 0
    for tree in sentence_trees:
        for pos in tree.treepositions():
            node = tree[pos]
            if type(node) is str:
                total += len(node)

    return total


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
            if not True in [c in token['word'].lower() for c in 'abcdefghijklmnopqrstuvwxyz']:
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


def count_nodes(terminal_count, non_terminal_count):
    return sum(terminal_count.values()) + sum(non_terminal_count.values())


def get_dependency_tree_depth(annotation):
    dt_depths = []
    for sentence in annotation['sentences']:
        deps = list(sentence['basicDependencies'])
        # deps = annotation['sentences'][0]['enhancedPlusPlusDependencies']

        depths = np.zeros(len(deps)+1)
        depths[0] = 1
        while len(deps) > 0:
            remaining_deps = []
            for i in range(0, len(deps)):
                dep = deps[i]
                if depths[dep['governor']] > 0:
                    depths[dep['dependent']] = depths[dep['governor']] + 1
                else:
                    remaining_deps.append(dep)

            deps = remaining_deps

        dt_depths.append(np.max(depths))

    return np.average(dt_depths)


def get_syntactic_features(annotation):
    num_sentences = len(annotation['sentences'])
    sentence_trees = [Tree.fromstring(sentence['parse']) for sentence in annotation['sentences']]
    terminal_count, non_terminal_count = count_tags(sentence_trees)
    type_count, token_count = count_types(annotation)
    node_count = count_nodes(terminal_count, non_terminal_count)

    tags = [
        # clause
        'S', 'SBAR', 'SBARQ', 'SINV', 'SQ',

        # phrase
        'ADJP', 'ADVP', 'CONJP', 'FRAG', 'INTJ', 'LST', 'NAC', 'NP', 'NX', 'PP', 'PRN', 'PRT', 'QP',
        'RRC', 'UCP', 'VP', 'WHADJP', 'WHAVP', 'WHNP', 'WHPP', 'X',

        # word
        'CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS',
        'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG',
        'VBN', 'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB'
    ]

    features = []

    for tag in tags:
        features.append(get_sum(non_terminal_count, [tag]) / token_count)
        features.append(get_sum(non_terminal_count, [tag]) / num_sentences)

    features.extend([
        # --------------- others ----------------
        # depth of dependency tree
        get_dependency_tree_depth(annotation),

        # number of non-terminal nodes per parse tree
        count_non_terminal_nodes(sentence_trees) / num_sentences,

        # type-token ratio
        type_count / token_count,
        type_count / (token_count ** 0.5),
        type_count / ((2 * token_count) ** 0.5),
        (math.log(token_count) - math.log(type_count)) / math.log(token_count) ** 0.5,
        type_count / num_sentences,

        # tokens per sentence
        token_count / num_sentences,

        # number of nodes
        node_count / num_sentences,
        node_count / token_count,

        # average node depth
        count_sum_node_depth(sentence_trees) / token_count,

        # average word length
        count_sum_word_length(sentence_trees) / token_count
    ])

    return features


if __name__ == '__main__':
    annotation = DataSet('cepp').load_stanford_annotation(0)

    # pprint.pprint(annotation)
    # sentence_trees = [Tree.fromstring(sentence['parse']) for sentence in annotation['sentences']]
    # sentence_trees[0].pretty_print()
    for sentence in annotation['sentences']:
        for token in sentence['tokens']:
            print(token['lemma'], token['word'], token['originalText'], token['pos'])

    print(count_types(annotation))

    # sys.exit()

    print(get_syntactic_features(annotation))
    print(len(get_syntactic_features(annotation)))
