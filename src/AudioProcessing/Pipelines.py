import numpy as np

'''
The "Pipeline" module contains the classes responsible for managing the "flow"
of audio data.
'''

class PipelineBase:
    '''
    Base class for all audio pipelines.
    '''
    def append_effect(self, eff):
        '''
        Adds an effect object to the end of the effect queue.
        '''
        raise NotImplementedError
