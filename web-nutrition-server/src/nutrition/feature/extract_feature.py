
import numpy as np
import time
from nutrition.structure.data_set import DataSet
from nutrition.structure.counter import Counter
from nutrition.feature import stanford_feature

def extract_features(text, annotation):
    return stanford_feature.get_features(annotation)
    
def process_feature(data_set, restart=False):
    if restart:
        feature_matrix = None
    else:
        # load features we have extracted so far
        # this would not be needed if we use append file instead of np.savetxt to store the feature matrix
        feature_matrix = data_set.load_feature_matrix()
        
    def save():
        data_set.save_feature_matrix(feature_matrix)

    # load count, i.e. how many documents have been parsed successfully
    counter = Counter(data_set.feature_path,
        commit_interval=50,
        on_commit=save,
        restart=restart)
    
    start = time.time()
    while counter.count < data_set.data['count']:
        doc_start = time.time()
        
        # read raw text and parse tree
        text = data_set.get_text(counter.count)
        label = data_set.data['labels'][counter.count]
        annotation = data_set.load_stanford_annotation(counter.count)
        
        # extract features into a row array
        row = extract_features(text, annotation)
        row.append(label)

        # initialize feature matrix if it is None
        if feature_matrix is None:
            feature_matrix = np.zeros([data_set.data['count'], len(row)])
            
        # insert row array to matrix
        feature_matrix[counter.count,:] = row
        
        # count and print
        counter.increment()
        print('%i, %i%% %.2f seconds (%.0f total))' % (counter.count-1, 100*counter.count/data_set.data['count'], time.time() - doc_start, time.time() - start))
        
    counter.commit()


if __name__ == '__main__':
    process_feature(DataSet('cepp'), restart=True)
