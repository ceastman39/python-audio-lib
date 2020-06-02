import numpy as np
class EffectPipe:
    '''
        Abstract class for all effects to be derived from.

        TODO: Write more documentation.
    '''
    def __init__(self, rate = 44100, ch = 2, dtype = np.int16, blocksize = 1024, dgain = 0.7, wgain = 0.3):
        '''

        Constructor.

        Parameters:
            rate: Sampling rate. Default: 44100
            ch: Number of channels. Default: 2
            dtype: Numpy data type. Default: np.int16
                   [np.int16, np.int32, np.float32]
           dgain: "Dry" gain ratio. Default: 0.7
           dgain: "Wet" gain ratio. Default: 0.3

        '''
        self.__RATE = rate
        if(dtype not in [np.int16, np.int32, np.float32]):
            eString = f'''\n\tdtype must be numpy.int16, numpy.int32, or numpy.float32. Type given: {dtype}'''
            raise TypeError(eString)
        self.__TYPE = np.dtype(dtype)
        self.__CHANNELS = ch
        self.__BLOCKSIZE = blocksize
        self.__DGAIN = dgain
        self.__WGAIN = wgain

    def push(self, data):
        '''

        Does an operation on the data, and pushes it to the queue.

        Parameters:
            data: Numpy array containing audio data.

        '''
        raise NotImplementedError

    def get(self):
        '''

        Returns the data from the queue.

        '''
        raise NotImplementedError

    def __add_effect(self, data):
        '''

        The internal function to be overridden that applies the effect to the
        audio data passed.

        Parameters:
            data: numpy array containing audio data.

        '''
        raise NotImplementedError


    #Properties
    ##region
    @property
    def rate(self):
        '''Returns the sampling rate being used.'''
        return self.__RATE

    @property
    def type(self):
        '''Returns the data type being used for the audio data.'''
        return self.__TYPE

    @property
    def channels(self):
        '''Returns the number of channels being used for the audio data.'''
        return self.__CHANNELS

    @property
    def gain(self):
        '''Returns a tuple containing both the dry and wet gain values. (Dry, Wet).'''
        return (self.__DGAIN, self.__WGAIN)

    @property
    def blocksize(self):
        '''Returns the size of the blocksize.'''
        return self.__BLOCKSIZE
    ##endregion
