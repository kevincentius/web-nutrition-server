'''
Created on May 23, 2018

@author: Eldemin
'''
import time

class Stopwatch(object):

    def __init__(self, name=None):
        self.name = name
        self.start_time = time.time()
        self.last_time = self.start_time
        self.lap_message = 'start'
        print('Stopwatch started: {}'.format(name))
    
    def lap(self, message):
        current_message = self.lap_message
        
        current_time = time.time()
        lap_time = current_time - self.last_time
        total_time = current_time - self.start_time
        self.last_time += lap_time
        self.lap_message = message
        print('Stopwatch {} ({:.2f} / {:.2f}) - {}'.format(self.name, lap_time, total_time, current_message))
    
    def show(self, message):
        current_time = time.time()
        lap_time = current_time - self.last_time
        total_time = current_time - self.start_time
        print('Stopwatch {} ({:.2f} / {:.2f}) - {}'.format(self.name, lap_time, total_time, message))
    
    def finish(self):
        current_time = time.time()
        lap_time = current_time - self.last_time
        total_time = current_time - self.start_time
        self.last_time += lap_time
        print('Stopwatch {} ({:.2f} / {:.2f}) - {}'.format(self.name, lap_time, total_time, self.lap_message))
    