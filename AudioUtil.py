import numpy as np
'''
Utility functions to be used when manipulating audio data.
'''

def add_samples(x, y):
    '''

    Adds two audio data sample.

    TODO: Add clipping prevention.

    Parameters:
        x: Numpy array to add to.
        y: Numpy array to add from.

    '''
    return np.add(x, y)
