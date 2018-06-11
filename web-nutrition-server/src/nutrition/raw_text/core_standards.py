import os

from nutrition.structure.data_set import DataSet

if __name__ == '__main__':

    data_set = DataSet('core-standard');
    raw_folder = 'D:/master project/dataold/core-standards-readability'
    grades = ['1', '2-3', '4-5', '6-8', '9-10', '11-CCR']
    bans = ['poetry', 'drama']

    labels = []

    text_id = 0
    for l in range(0, 6):
        print('working on level', l)
        path_level = raw_folder + '/grade ' + grades[l]
        for cat in os.listdir(path_level):
            path_cat = path_level + '/' + cat
            if any(ban in cat for ban in bans):
                print('ignoring ' + path_cat)
            else:
                for file in os.listdir(path_cat):
                    path_text = path_cat + '/' + file
                    print('reading ' + path_text)
                    data_set.import_raw_text(path_text, text_id)
                    labels.append(l)
                    text_id += 1

    data_set.set_labels(labels)