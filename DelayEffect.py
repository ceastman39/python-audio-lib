from EffectPipe import EffectPipe
from collections import deque
import numpy as np
import AudioUtil as au

class DelayEffect(EffectPipe):
    '''
        Delay Effect.

        TODO: Write more documentation.
    '''
    def __init__(self, rate, ch, dtype, time=500):
        '''

        Constructor

        Parameters:
            rate: Sampling rate. Default: 44100
            ch: Number of channels. Default: 2
            dtype: Numpy data type. Default: np.int16
                   [np.int16, np.int32, np.float32]
            time: Delay in milliseconds.

        Note: Types are enforced in the base class EffectPipe

        '''
        super().__init__(rate, ch, dtype)
        self.__queue = deque()
        self.__delay_queue = deque(np.zeros(time*(self.rate // 1000), dtype=self.type))

    def push(self, data):
        '''

        Public function to push data to the pipeline.

        '''
        if(data.dtype is not self.type):
            eString = f"Given data needs to have the same type as the DelayEffect. Type needed: {self.type}, type given: {data.dtype}"
            raise TypeError

        self.__queue.append(self.__add_effect(data))
        return

    def get(self):
        '''

        Returns the data from the queue in the form of a numpy array.

        '''
        if(len(self.__queue) > 0):
            return self.__queue.popleft()
        else:
            return None

    def __add_effect(self, data):
        '''

        The function that modifies the data as it's being pushed.

        Parameters:
            data: numpy array containing audio data.

        '''
        effect_data = np.empty(shape=data.shape, dtype=self.type)
        for i in range(data.shape[0]):
            self.__delay_queue.append(data[i][0])
            effect_data[i][0] = self.__delay_queue.popleft()

        return au.add_samples(data, effect_data)
