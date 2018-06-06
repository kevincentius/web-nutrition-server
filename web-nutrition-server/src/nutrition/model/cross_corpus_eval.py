
from sklearn import linear_model
from sklearn.linear_model import Ridge, Lasso
from sklearn.model_selection import train_test_split
from sklearn.model_selection._validation import cross_val_score

import matplotlib.pyplot as plt
from sklearn.svm import SVR, SVC

from nutrition.structure.data_set import DataSet
import pickle
from nutrition.structure.environment import ROOT_FOLDER

from sklearn.feature_selection import RFE
from pprint import pprint
from sklearn.linear_model.base import LinearRegression

import numpy as np
import sys
from nutrition.feature.stanford_feature import get_feature_names
from math import sqrt

def eval_plot(model, data_set, cc_set, features):
    x, y = data_set.load_training_data()
    x = x[:, features]

    # cross validation
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4, shuffle=True, random_state=0)
    model.fit(x_train, y_train)
    cv_predict = model.predict(x_test)
    plt.figure()
    plt.scatter(y_test, cv_predict)
    plt.title('CEPP: Cross validation')
    print("Cross Validation RMSE: {}".format(sqrt(sum((y_test-cv_predict)**2))))

    print(sum(abs(y_test-cv_predict) < 0.5) / len(y))

    # train set performance
    model.fit(x, y)
    predict_train = model.predict(x)
    #plt.figure()
    #plt.scatter(y, predict_train)
    #plt.title('Train set')

    # cross corpus
    x_cc, y_cc = cc_set.load_training_data()
    x_cc = x_cc[:, features]
    cc_predict = model.predict(x_cc)
    plt.figure()
    plt.scatter(y_cc, cc_predict)
    plt.title('CEPP model on Newsela')

    plt.show()


if __name__ == '__main__':
    model = SVC(kernel='linear')
    data_set = DataSet('cepp')
    cc_set = DataSet('core-standard')

    # features = [6,66,69,86,112,115,118,121]  # RFE
    # features = [120, 121, 66, 68, 115, 45]  # Greedy
    # features = [15, 31]  # NP/VP per sentence
    features = list(range(0, 122))

    eval_plot(model, data_set, cc_set, features)