
import numpy as np
import time
from nutrition.structure.data_set import DataSet
from nutrition.structure.counter import Counter
from nutrition.feature import stanford_feature

class FeatureExtractor(object):
    
    def save(self):
        self.data_set.save_feature_matrix(self.feature_matrix)
    
    def extract_features(self, text, annotation):
        return stanford_feature.get_features(annotation)
        
    def process_data_set(self, data_set, restart=False):
        self.data_set = data_set
        
        # load features we have extracted so far
        # this would not be needed if we use append file instead of np.savetxt to store the feature matrix
        if not restart:
            self.feature_matrix = self.data_set.load_feature_matrix()
            
        # load count, i.e. how many documents have been parsed successfully
        counter = Counter(data_set.feature_path,
            commit_interval=50,
            on_commit=self.save,
            restart=restart)
        
        start = time.time()
        while counter.count < data_set.data['count']:
            doc_start = time.time()
            
            # read raw text and parse tree
            text = data_set.get_text(counter.count)
            label = data_set.data['labels'][counter.count]
            annotation = data_set.load_stanford_annotation(counter.count)
            
            # insert row to matrix
            # also, initialize feature matrix if it is None
            row = self.extract_features(text, annotation)
            row.append(label)

            if not hasattr(self, 'feature_matrix'):
                self.feature_matrix = np.zeros([data_set.data['count'], len(row)])
            self.feature_matrix[counter.count,:] = row
            
            # count and print
            counter.increment()
            print('%i, %i%% %.2f seconds (%.0f total))' % (counter.count-1, 100*counter.count/data_set.data['count'], time.time() - doc_start, time.time() - start))
            
        counter.commit()

if __name__ == '__main__':
    FeatureExtractor().process_data_set(DataSet('cepp'))
    