
import matplotlib.pyplot as plt
import sklearn

from nutrition.structure.data_set import DataSet
import pickle
from nutrition.structure.environment import ROOT_FOLDER

from sklearn.feature_selection import RFE
from pprint import pprint
from sklearn.linear_model.base import LinearRegression

import numpy as np
import sys
from nutrition.feature.stanford_feature import get_feature_names


if __name__ == '__main__':
    x, y = DataSet('cepp').load_training_data()
    mi = sklearn.feature_selection.mutual_info_regression(x, y)
    row_id = list(range(0, len(x[0])))

    print(len(mi), len(row_id))

    mat = np.column_stack((mi, row_id))
    #mat = np.sort(mat, axis=0)

    mat = mat[mat[:, 0].argsort()]

    print(mat)

