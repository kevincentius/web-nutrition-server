import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from nutrition.structure.data_set import DataSet

if __name__ == '__main__':
    # open data set
    data_set = DataSet('cepp')

    # get train and test set
    x, y = data_set.load_training_data();
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5, shuffle=True, random_state=0)

    # train and save model
    model = RandomForestClassifier(n_estimators=1000, oob_score=True, warm_start=True)
    model.fit(x_train, y_train)
    data_set.save_model(model, 'random-forest')

    # get cross validation performance
    predict = model.predict(x_test)
    print('Cross validation accuracy:', accuracy_score(y_test, predict))

    # print classification result as a matrix
    num_classes = 5
    class_mat = np.zeros([num_classes, num_classes])
    distances = np.zeros(num_classes)
    for i in range(0, len(y_test)):
        class_mat[int(predict[i]), int(y_test[i])] += 1
        distances[int(abs(predict[i] - y_test[i]))] += 1

    print('Classification matrix: \n', class_mat)
    print('Distances:', distances)

