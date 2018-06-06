import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from nutrition.structure.data_set import DataSet

if __name__ == '__main__':
    x, y = DataSet('cepp').load_training_data()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5, shuffle=True, random_state=0)

    model = RandomForestClassifier(n_estimators=1000, oob_score=True, warm_start=True)

    model.fit(x_train, y_train)
    predict = model.predict(x_test)
    print(accuracy_score(y_test, predict))

    class_mat = np.zeros([5, 5])
    print(class_mat)

    for i in range(0, len(y_test)):
        class_mat[int(predict[i]), int(y_test[i])] += 1

    print(class_mat)