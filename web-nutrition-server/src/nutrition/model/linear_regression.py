
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.model_selection._validation import cross_val_score

import matplotlib.pyplot as plt
from nutrition.structure.data_set import DataSet
import pickle
from nutrition.structure.environment import ROOT_FOLDER

def train_linear(data_set):
    # load training data from feature matrix
    x, y  = data_set.load_training_data()
    
    # train model fully
    model = linear_model.LinearRegression(normalize=True)
    model.fit(x, y)
    
    return model

# trains and save model
def create_linear(data_set):
    model = train_linear(data_set)
    
    fn = '{}/_model/lin_{}'.format(ROOT_FOLDER, data_set.name)
    
    with open(fn, 'wb') as file:
        pickle._dump(model, file)
    
    print('Model saved in {}'.format(fn))
    
    return model

def eval_linear(data_set, test_size=0.4):
    # load training data from feature matrix
    x, y  = data_set.load_training_data()
    
    # split data into train and test set
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, shuffle=True, random_state=0)
    
    # train model on train set
    model = linear_model.LinearRegression(normalize=True)
    model.fit(x_train, y_train)
    
    # evaluate on test set
    score = cross_val_score(model, x_test, y_test, scoring='neg_mean_squared_error')
    print('Mean squared error: {}'.format(-score))
    
    # plot
    predict = model.predict(x_test)
    plt.scatter(y_test, predict)
    plt.show()

def eval_cc_linear(train_data_set, test_data_set):
    # train model on train data set
    model = train_linear(train_data_set)
    
    # evaluate model on test data set (cross corpus)
    x, y  = test_data_set.load_training_data()
    score = cross_val_score(model, x, y, scoring='neg_mean_squared_error')
    print('Mean squared error: {}'.format(-score))
    
    # plot
    predict = model.predict(x)
    plt.scatter(y, predict)
    plt.show()


if __name__ == '__main__':
    data_set = DataSet('cepp')
    
    x, y  = data_set.load_training_data()
    
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4, shuffle=True, random_state=0)
    
    regr = linear_model.LinearRegression(normalize=True)
    #regr = linear_model.Ridge(alpha=0.001, normalize=True)
    
    regr.fit(x_train, y_train)
    predict = regr.predict(x_test)
    
    scores = cross_val_score(regr, x_test, y_test, scoring='neg_mean_squared_error')
    print(scores.mean())
    
    plt.scatter(y_test, predict)
    plt.show()
    