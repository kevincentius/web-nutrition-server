
from nutrition.structure.data_set import DataSet
import numpy as np

if __name__ == '__main__':
    data_set = DataSet('newsela')
    
    labels = np.genfromtxt('D:/master project/data/newsela/average_level.csv', delimiter=',')
    data_set.set_labels(labels[:,1].tolist())
    
    for i in range(0, 17027):
        path = 'D:/master project/data/newsela/text/{}.txt'.format(i+1)
        data_set.import_raw_text(path, i)
        
        print(i)
    
    