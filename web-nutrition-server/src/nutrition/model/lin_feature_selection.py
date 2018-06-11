from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt
from nutrition.structure.data_set import DataSet

from sklearn.linear_model.base import LinearRegression

import numpy as np
from nutrition.readability.stanford_feature import get_feature_names


def get_error(x, y):
    model = LinearRegression(normalize=True)
    model.fit(x, y)
    predict = model.predict(x)
    return np.average(np.abs(y - predict))


def get_cv_error(x_train, x_test, y_train, y_test):
    model = LinearRegression(normalize=True)
    model.fit(x_train, y_train)
    predict = model.predict(x_test)
    return np.average(np.abs(y_test - predict))


def forward_feature_selection(data_set, cross_data_set):
    x, y = data_set.load_training_data()

    # data to plot later
    plot_x_num_features = []
    plot_y_error = []
    plot_y_cv_error = []

    # split data into train and test set
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4, shuffle=True, random_state=0)

    print(get_cv_error(x_train, x_test, y_train, y_test))

    feature_ids_left = list(range(0, len(x_train[0])))
    feature_ids = []
    features = get_feature_names()  # list(range(0, len(x_train[0])))

    while len(feature_ids_left) > 0:
        # find most important feature to add
        b_id = -1
        b_error = -1
        b_cv_error = -1

        # fid = index in feature_ids_left
        for fid in range(0, len(feature_ids_left)):
            # feature ids to test
            c_feature_ids = feature_ids.copy()
            c_feature_ids.append(feature_ids_left[fid])
            c_feature_ids = sorted(c_feature_ids)

            # get sub matrices
            c_x_train = x_train[:, c_feature_ids]
            c_x_test = x_test[:, c_feature_ids]

            # calculate error
            c_error = get_error(c_x_train, y_train)

            if b_error == -1 or b_error > c_error:
                b_id = fid
                b_error = c_error
                b_cv_error = get_cv_error(c_x_train, c_x_test, y_train, y_test)

        # update feature list
        feature_ids.append(feature_ids_left.pop(b_id))
        print([features[i] for i in feature_ids], feature_ids, b_error, b_cv_error, len(feature_ids))

        # add data to plot list
        plot_x_num_features.append(len(feature_ids))
        plot_y_error.append(b_error)
        plot_y_cv_error.append(b_cv_error)

    # print(features, b_error)
    plt.scatter(plot_x_num_features, plot_y_error)
    plt.scatter(plot_x_num_features, plot_y_cv_error)
    plt.show()


def backward_feature_selection(data_set, cross_data_set):
    x, y = data_set.load_training_data()

    # data to plot later
    plot_x_num_features = []
    plot_y_error = []
    plot_y_cv_error = []
    
    # split data into train and test set
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4, shuffle=True, random_state=0)
    
    print(get_cv_error(x_train, x_test, y_train, y_test))
    
    target_num_features = 1
    feature_ids = list(range(0, len(x_train[0])))
    features = get_feature_names() # list(range(0, len(x_train[0])))
    while len(x_train[0]) > target_num_features:
        # find least important feature to remove
        b_id = -1
        b_error = -1
        b_cv_error = -1

        # c = current column id
        for c in range(0, len(x_train[0])):
            c_x_train = np.delete(x_train, c, 1)
            c_x_test = np.delete(x_test, c, 1)
            c_error = get_error(c_x_train, y_train)
            
            if b_error == -1 or b_error > c_error:
                b_id = c
                b_error = c_error
                b_cv_error = get_cv_error(c_x_train, c_x_test, y_train, y_test)
        
        x_train = np.delete(x_train, b_id, 1)
        x_test = np.delete(x_test, b_id, 1)
        features = np.delete(features, b_id, 0)
        feature_ids = np.delete(feature_ids, b_id, 0)
        print(features, feature_ids, b_error, b_cv_error, len(x_train[0]))
        plot_x_num_features.append(len(x_test[0]))
        plot_y_error.append(b_error)
        plot_y_cv_error.append(min(10, b_cv_error))
        
    #print(features, b_error)
    plt.scatter(plot_x_num_features, plot_y_error)
    plt.scatter(plot_x_num_features, plot_y_cv_error)
    plt.show()
    
    
if __name__ == '__main__':
    #backward_feature_selection(DataSet('cepp'), DataSet('mini-newsela'))
    forward_feature_selection(DataSet('cepp'), DataSet('mini-newsela'))
