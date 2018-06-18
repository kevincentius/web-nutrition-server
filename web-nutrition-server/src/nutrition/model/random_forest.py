import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from nutrition.structure.data_set import DataSet


def train_model(x, y):
    model = RandomForestClassifier(n_estimators=1000, oob_score=True, warm_start=True)
    model.fit(x, y)
    return model


def print_classification_matrix(predict, y_test):
    # print classification result as a matrix
    num_classes = 10
    class_mat = np.zeros([num_classes, num_classes])
    distances = np.zeros(num_classes)
    for i in range(0, len(y_test)):
        class_mat[int(predict[i]), int(y_test[i])] += 1
        distances[int(abs(predict[i] - y_test[i]))] += 1
    print('Classification matrix: \n', class_mat)
    print('Distances:', distances)


def cross_validation(data_set_name):
    # open data set
    data_set = DataSet(data_set_name)

    # get train and test set
    x, y = data_set.load_training_data();
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, shuffle=True)

    # train and save model
    model = train_model(x_train, y_train)

    # get cross validation performance
    predict = model.predict(x_test)
    accuracy = accuracy_score(y_test, predict)
    print('Cross validation accuracy:', accuracy)

    print_classification_matrix(predict, y_test)

    return accuracy


def leave_one_out_score(data_set_name):
    # open data set
    data_set = DataSet(data_set_name)
    x, y = data_set.load_training_data();

    correct_count = 0

    for i in range(len(y)):
        x_train = np.delete(x, i, axis=0)
        y_train = np.delete(y, i)
        x_test = [x[i]]
        y_test = [y[i]]

        # train model
        model = train_model(x_train, y_train)
        if model.predict(x_test)[0] == y_test:
            correct_count += 1
            print(i, 'correct,', correct_count / (i+1))
        else:
            print(i, 'wrong,', correct_count / (i+1))

    print('accuracy:', correct_count / len(y))


def cross_corpus(train_set_name, test_set_name):
    # open data set and train model
    train_set = DataSet(train_set_name)
    x_train, y_train = train_set.load_training_data()
    model = train_model(x_train, y_train)

    # open test set and predict labels
    test_set = DataSet(test_set_name)
    x_test, y_test = test_set.load_training_data()
    predict = model.predict(x_test)

    print_classification_matrix(predict, y_test)

    return model


if __name__ == '__main__':
    # which data set to use
    train_on = 'cepp'
    test_on = 'cepp'
    num_trials = 100

    # evaluate model
    # leave_one_out_score('cepp')

    total_acc = 0
    accs = []
    for i in range(0, num_trials):
        accs.append(cross_validation(train_on))
    print('accs:' + accs)
    print('average cross validation accuracy:', sum(accs)/num_trials)

    model = cross_corpus(train_on, test_on)

    # save fully trained model
    # DataSet(train_on).save_model(model, 'random-forest')