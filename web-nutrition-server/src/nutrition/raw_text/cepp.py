
from nutrition.structure.data_set import DataSet

if __name__ == '__main__':
    
    data_set = DataSet('cepp')
    
    levels = ['KET', 'PET', 'FCE', 'CAE', 'CPE']
    num_articles = [64, 60, 71, 67, 69]
    
    labels = []
    
    text_id = 0
    for l in range(0, 5):
        print('working on level', l)
        for i in range(1, num_articles[l] + 1):
            print('working on text', i)
            path = '{}/_origin/{}/{}.txt'.format(data_set.path, levels[l], i)
            data_set.import_raw_text(path, text_id)
            labels.append(l)
            text_id += 1
            
    data_set.set_labels(labels)
    
