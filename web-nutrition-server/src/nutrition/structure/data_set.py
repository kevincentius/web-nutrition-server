
import os
from shutil import copyfile

import numpy as np
import json
import pickle
from nutrition.structure.counter import Counter
from nutrition.structure.environment import ROOT_FOLDER

class DataSet(object):

    def __init__(self, name):
        self.name = name
        
        # set paths
        self.path = ROOT_FOLDER + '/' + self.name
        self.raw_text_path = self.path + '/raw_text'
        self.data_path = self.raw_text_path + '/_data.json'
        self.stanford_path = self.path + '/stanford'
        self.feature_path = self.path + '/feature'
        self.model_path = self.path + '/model'
        
        # create folders if not exist
        for path in [
            self.path,
            self.raw_text_path,
            self.stanford_path,
            self.feature_path,
            self.model_path
        ]:
            if not os.path.exists(path):
                os.makedirs(path)
                
        # load data
        if os.path.exists(self.data_path):
            with open(self.data_path, 'r', encoding='utf8') as json_file:  
                self.data = json.load(json_file)
        else:
            self.data = {}
        
        # load labels
        if os.path.exists(self.data_path):
            with open(self.data_path, 'r', encoding='utf8') as json_file:  
                self.labels = json.load(json_file)
    
    # Copies the file with the given path into the data set directory
    # This makes the file usable by other scripts.
    def import_raw_text(self, path, text_id):
        copyfile(path, self.raw_text_path + '/' + str(text_id))
    
    # When importing raw_text, the labels must be set as well.
    # labels is an array of numbers
    def set_labels(self, labels):
        self.labels = np.array(labels)
        self.data['count'] = len(labels)
        self.data['labels'] = labels
        with open(self.data_path, 'w') as json_file:  
            json.dump(self.data, json_file)
    
    
    # load text from raw_text folder
    def get_text(self, text_id):
        with open(self.raw_text_path + '/' + str(text_id), 'r', encoding='utf8') as file:
            return file.read()

    # save annotation (stanford parse tree) into the stanford folder
    def save_stanford_annotation(self, text_id, annotation):
        with open('{}/{}'.format(self.stanford_path, text_id), 'wb') as file:
            pickle.dump(annotation, file)

    # load annotation (stanford parse tree) from the stanford folder
    def load_stanford_annotation(self, text_id):
        with open('{}/{}'.format(self.stanford_path, text_id), 'rb') as file:
            return pickle.load(file)

    # each row in the matrix represents one training data
    def save_feature_matrix(self, mat):
        with open('{}/features.csv'.format(self.feature_path), 'wb') as file:
            np.savetxt(file, mat)
        
    # if does not exists, returns None
    def load_feature_matrix(self):
        path = '{}/features.csv'.format(self.feature_path)
        if os.path.exists(path):
            with open(path, 'rb') as file:
                return np.loadtxt(file)

    def load_training_data(self):
        feature_matrix = self.load_feature_matrix()
        
        num_features = len(feature_matrix[0]) - 1
        x = feature_matrix[:, 0:num_features]
        y = feature_matrix[:, num_features]
        
        return x, y

    def print_info(self):
        if hasattr(self, 'data'):
            print('raw text: {} files'.format(self.data['count']))
        else:
            print('raw text: none')
        
        
        stanford_counter = Counter(self.stanford_path)
        if stanford_counter.count > 0:
            print('stanford parse: {}'.format(stanford_counter.count))
        else:
            print('stanford parse: none')
        
        
        feature_counter = Counter(self.feature_path)
        if feature_counter.count > 0:
            print('feature extraction: {}'.format(feature_counter.count))
        else:
            print('feature extraction: none')
