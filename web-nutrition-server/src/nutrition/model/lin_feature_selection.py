
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.model_selection._validation import cross_val_score

import matplotlib.pyplot as plt
from nutrition.structure.data_set import DataSet
import pickle
from nutrition.structure.environment import ROOT_FOLDER

from sklearn.feature_selection import RFE
from pprint import pprint
from sklearn.linear_model.base import LinearRegression

import numpy as np
import sys

def get_error(x, y):
    model = LinearRegression(normalize=True)
    model.fit(x, y)
    predict = model.predict(x)
    return np.average((y - predict)**2)

def get_cv_error(x_train, x_test, y_train, y_test):
    model = LinearRegression(normalize=True)
    model.fit(x_train, y_train)
    predict = model.predict(x_test)
    return np.average((y_test - predict)**2)

def test_feature_selection(data_set):
    x, y  = data_set.load_training_data()
    
    # data to plot later
    plot_x_num_features = []
    plot_y_cv_error = []
    
    # split data into train and test set
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4, shuffle=True, random_state=0)
    
    print(get_cv_error(x_train, x_test, y_train, y_test))
    
    target_num_features = 1
    features = list(range(0, len(x_train[0])))
    while len(x_train[0]) > target_num_features:
        # find least important feature to remove
        b_id = -1
        b_error = -1
        
        # c = current column id
        for c in range(0, len(x_train[0])):
            c_x_train = np.delete(x_train, c, 1)
            c_x_test = np.delete(x_test, c, 1)
            c_error = get_cv_error(c_x_train, c_x_test, y_train, y_test)
            
            if b_error == -1 or b_error > c_error:
                b_id = c
                b_error = c_error
        
        x_train = np.delete(x_train, b_id, 1)
        x_test = np.delete(x_test, b_id, 1)
        features = np.delete(features, b_id, 0)
        print(features, b_error)
        plot_x_num_features.append(len(x_test[0]))
        plot_y_cv_error.append(b_error)
        
    #print(features, b_error)
    plt.scatter(plot_x_num_features, plot_y_cv_error)
    plt.show()
    
    
if __name__ == '__main__':
    test_feature_selection(DataSet('cepp'))
