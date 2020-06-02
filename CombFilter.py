from EffectPipe import EffectPipe
from collections import deque
import numpy as np
import AudioUtil as au

class CombFilter(EffectPipe):
    '''
        A Comb Filter.

        TODO: Write more documentation.
    '''
    def __init__(self, rate = 44100, ch = 2, dtype = np.int16, blocksize = 1024, dgain = 0.7, wgain = 0.7, time=100):
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
        super().__init__(rate, ch, dtype, blocksize, dgain, wgain)
        self.__queue = deque()
        self.__delay_queues = [deque(np.zeros((time*(rate//1000)), dtype=self.type)) for i in range(ch)]
        self.__last_sample = np.zeros(shape=(blocksize, ch), dtype=self.type)

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
        effect_data = np.empty(shape=data.shape, dtype=self.type)
        for i in range(self.blocksize):
            for j in range(self.channels):
                effect_data[i][j] = self.__delay_queues[j].popleft()
                self.__delay_queues[j].append(au.add_samples_gain(data[i][j], effect_data[i][j], self.gain[1]))

        return au.add_samples_gain(data, effect_data, 0.7)
