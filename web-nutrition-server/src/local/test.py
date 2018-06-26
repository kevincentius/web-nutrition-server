from nltk.corpus import stopwords

from nutrition.structure.data_set import DataSet

if __name__ == '__main__':
    DataSet('learning-corpus').delete_row(1437)
