import os

from nutrition.structure.data_set import DataSet

if __name__ == '__main__':
    levels = ['elementry', 'pre_inter', 'intermediate', 'upper_inter', 'advanced']

    data_set = DataSet('learning-corpus')
    labels = []

    text_id = 0
    root_path = 'D:/master project/dataold/learning_corpus'
    for level in range(len(levels)):
        level_path = root_path + '/' + levels[level]

        for file_name in os.listdir(level_path):
            text_path = level_path + '/' + file_name

            with open(text_path, 'r', encoding='utf8') as file:
                text_length = len(file.read())

            if 10 < text_length < 100000:
                labels.append(level)
                data_set.import_raw_text(text_path, text_id)
                text_id += 1

    data_set.set_labels(labels)


