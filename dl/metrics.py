import matplotlib.pyplot as plt
import numpy as np

class Aggregator():

        # log set of statistics to track 
        def __init__(self):
            self.stats = {}
            self.fns = {}
        
        def _buffer(self, input):
            return input
        
        def addStat(self, stat, fn=None):
            if fn is None: self.fns[stat] = self._buffer
            else: self.fns[stat] = fn
            self.stats[stat] = []
            
        def logStat(self, stat, args):
            self.stats[stat].append(self.fns[stat](*args))
        
        # return specific statistic logged history
        def getStats(self, stat):
            return self.stats[stat]
        
class Plotter():
    
    def chart(x_value, y_value, x_label, y_label, title):
        plt.plot(y_value, x_value)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()
        plt.close()
        
    def plot(train, val, x_label, y_label, title):
        plt.plot(np.arange(1, len(train)+1), train)
        plt.plot(np.arange(1, len(val)+1), val)
        plt.legend(['Training', 'Validation'])
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()
        plt.close()