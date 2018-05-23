import os

class Counter(object):

    def __init__(self, folder, commit_interval=1, on_commit=None):
        self.path = folder + '/_count'
        self.commit_interval = commit_interval
        self.pending = 0
        self.on_commit = on_commit
        
        # load count, i.e. how many documents have been parsed successfully
        if os.path.exists(self.path):
            with open(self.path, 'r') as count_file:
                self.count = int(count_file.read())
        else:
            self.count = 0
    
    def increment(self):
        self.count += 1
        self.pending += 1
        
        if self.pending >= self.commit_interval:
            self.commit()
            
    def commit(self):
        if self.on_commit is not None:
            self.on_commit()
        
        with open(self.path, 'w') as count_file:
            count_file.write(str(self.count))
        
        self.pending = 0