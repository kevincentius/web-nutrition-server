
# This class provides access to a data set's folder content, and is meant to keep all
# data sets in the same structure and avoid data-set-specific code.

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
        # if os.path.exists(self.data_path):
        #     with open(self.data_path, 'r', encoding='utf8') as json_file:
        #         self.labels = json.load(json_file)
    
    # Copies the file with the given path into the data set directory
    # This makes the file usable by other scripts.
    def import_raw_text(self, path, text_id):
        copyfile(path, self.raw_text_path + '/' + str(text_id))
    
    # When importing raw_text, the labels must be set as well.
    # labels is an array of numbers
    def set_labels(self, labels):
        # self.labels = np.array(labels)
        self.data['count'] = len(labels)
        self.data['labels'] = labels
        self.save_data()

    def save_data(self):
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

    # each row contains all features and the label as the last column
    def save_feature_matrix(self, mat):
        with open('{}/features.csv'.format(self.feature_path), 'wb') as file:
            np.savetxt(file, mat)
        
    # if does not exists, returns None
    def load_feature_matrix(self):
        path = '{}/features.csv'.format(self.feature_path)
        if os.path.exists(path):
            with open(path, 'rb') as file:
                return np.loadtxt(file)

    # returns features array (2D, each row is a training example) and labels array
    def load_training_data(self):
        feature_matrix = self.load_feature_matrix()
        
        num_features = len(feature_matrix[0]) - 1
        x = feature_matrix[:, 0:num_features]
        y = feature_matrix[:, num_features]
        
        return x, y

    # saves a trained model in the data set's folder. See also load_model(...)
    def save_model(self, model, name):
        filename = '{}/{}'.format(self.model_path, name)
        with open(filename, 'wb') as file:
            pickle.dump(model, file)

    def load_model(self, name):
        filename = '{}/{}'.format(self.model_path, name)
        with open(filename, 'rb') as file:
            return pickle.load(file)

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

    # BE CAREFUL when using this method
    # This method will remove the n-th training data, by:
    #   1 replacing it with the last training data
    #   2 removing the last training data
    def delete_row(self, text_id, delete_raw_text=True, delete_stanford_annotation=True):
        last_id = len(self.data['labels']) - 1

        if delete_raw_text:
            print('deleting raw_text', text_id)
            self.delete_and_replace_last(text_id, self.raw_text_path)

        if delete_stanford_annotation:
            print('deleting annotation', text_id)
            self.delete_and_replace_last(text_id, self.stanford_path)

        # update labels
        print('deleting label', text_id)
        self.data['labels'][text_id] = self.data['labels'][last_id]
        self.data['labels'].pop()
        self.data['count'] = len(labels)
        self.save_data()


    def delete_and_replace_last(self, text_id, folder):
        last_id = len(self.data['labels']) - 1

        current_file = folder + '/' + str(text_id)
        last_file = folder + '/' + str(last_id)

        # delete raw text
        os.rename(current_file, current_file + '_deleted')

        # replace raw text with last text
        copyfile(last_file, current_file)

        # delete last text
        os.rename(last_file, last_file + '_moved_as_' + str(text_id))

