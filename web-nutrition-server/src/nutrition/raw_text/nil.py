from nutrition.structure.data_set import DataSet
import os

if __name__ == '__main__':
    
    data_set = DataSet('nil')
    
    text_id = 0
    labels = []
    for level in range(1, 4):
        folder = 'D:/master project/data/news_in_levels/News_in_levels_level{}/articles/'.format(level)
        for filename in os.listdir(folder):
            # ignore files that are very small (< n bytes)
            if os.stat(folder+filename).st_size < 10:
                print('ignored {} because its size is only {} bytes'.format(folder+filename, os.stat(folder+filename).st_size))
                continue
                
            data_set.import_raw_text(folder + filename, text_id)
            labels.append(level)
            text_id += 1
            print(text_id)
            
    data_set.set_labels(labels)
    