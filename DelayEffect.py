from EffectPipe import EffectPipe
from collections import deque
import numpy as np

DRY_GAIN = 0
WET_GAIN = 1

class DelayEffect(EffectPipe):
    '''
        Delay Effect.

        TODO: Write more documentation.
    '''
    def __init__(self, rate, ch, dtype, dgain = 0.7, wgain = 0.5, time=250):
        '''

        Constructor

        Parameters:
            rate: Sampling rate. Default: 44100
            ch: Number of channels. Default: 2
            dtype: Numpy data type. Default: np.int16
                [np.int16, np.int32, np.float32]
            wgain: Wet gain ratio. Default: 0.5
            dgain: Dry gain ration. Default: 0.7
            time: Delay in milliseconds. Default: 500

        Note: Types for the default constructor arguments are enforced
              in the base class EffectPipe

        '''
        super().__init__(rate, ch, dtype, dgain, wgain)
        self.__ms = rate // 1000
        self.__delay = np.zeros(shape=(time*self.__ms,ch), dtype=(self.type))
        self.__queue = deque()

    def push(self, data):
        '''

        Public function to push data to the pipeline.

        Parameters:
            data: A numpy array containing audio data.

        '''
        if(data.dtype is not self.type):
            eString = f"Given data needs to have the same type as the DelayEffect. Type needed: {self.type}, type given: {data.dtype}"
            raise TypeError(eString)

        self.__queue.append(self.__add_effect(data))
        return

    def get(self):
        '''

        Returns the data from the queue in the form of a numpy array.

        Returns:
            A numpy array containing audio data, if there is data in the queue.
            None if no data is available.

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

        Returns:
            A numpy array containing manipulated audio data.

        '''
        data_size = data.shape[0]
        dry_data = (data * self.gain[DRY_GAIN]).astype(self.type)
        if(self.__delay.shape[0] < data_size):
            self.__delay = np.append(self.__delay, in_data[:(data_size - self.__delay.shape[0])], axis=0)
        wet_data = (self.__delay[:data_size] * self.gain[WET_GAIN]).astype(self.type)
        self.__delay = np.append(self.__delay[data_size:], data, axis=0)
        return np.add(dry_data, wet_data)
