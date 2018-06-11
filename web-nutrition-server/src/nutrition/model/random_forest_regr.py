from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from nutrition.structure.data_set import DataSet

import matplotlib.pyplot as plt

if __name__ == '__main__':
    x, y = DataSet('cepp').load_training_data()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5, shuffle=True, random_state=42)

    model = RandomForestRegressor(n_estimators=1000, oob_score=True, warm_start=True)

    model.fit(x_train, y_train)
    predict = model.predict(x_test)
    # print(accuracy_score(y_test, predict))

    plt.figure()
    plt.scatter(y_test, predict)
    plt.show()

