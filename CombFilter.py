from EffectPipe import EffectPipe
from collections import deque
import numpy as np

DRY_GAIN = 0
WET_GAIN = 1

class CombFilter(EffectPipe):
    '''
        A Comb Filter.

        TODO: Write more documentation.
    '''
    def __init__(self, rate, ch, dtype, dgain = 0.7, wgain = 0.7, decay = 0.9, time=100):
        '''

        Constructor.

        Parameters:
            rate: Sampling rate. Default: 44100
            ch: Number of channels. Default: 2
            dtype: Numpy data type. Default: np.int16
                   [np.int16, np.int32, np.float32]
           dgain: "Dry" gain ratio. Default: 0.7
           dgain: "Wet" gain ratio. Default: 0.7

        '''
        super().__init__(rate, ch, dtype, dgain, wgain)
        self.__ms = rate // 1000
        self.__delay = np.zeros(shape=(time*self.__ms,ch), dtype=(self.type))
        self.__queue = deque()
        self.__decay = decay

    def push(self, data):
        '''

        Does an operation on the data, and pushes it to the queue.

        Parameters:
            data: Numpy array containing audio data.

        '''
        if(data.dtype is not self.type):
            eString = f"Given data needs to have the same type as the DelayEffect. Type needed: {self.type}, type given: {data.dtype}"
            raise TypeError(eString)

        self.__queue.append(self.__add_effect(data))
        return

    def get(self):
        '''

        Returns the data from the queue.

        '''
        if(len(self.__queue) > 0):
            return self.__queue.popleft()
        else:
            return None

    def __add_effect(self, data):
        '''

        The internal function to be overridden that applies the effect to the
        audio data passed.

        Parameters:
            data: numpy array containing audio data.

        '''
        data_size = data.shape[0]
        dry_data = (data * self.gain[DRY_GAIN]).astype(self.type)
        append_data = (data * self.__decay).astype(self.type)
        if(self.__delay.shape[0] < data_size):
            self.__delay = np.append(self.__delay, data[:(data_size - self.__delay.shape[0])], axis=0)
        wet_data = (self.__delay[:data_size] * self.gain[WET_GAIN]).astype(self.type)
        self.__delay = np.append(self.__delay[data_size:], np.add(append_data, wet_data), axis=0)
        return np.add(dry_data, wet_data)
