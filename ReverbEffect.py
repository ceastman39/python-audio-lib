from EffectPipe import EffectPipe
from DelayEffect import DelayEffect
from CombFilter import CombFilter
from collections import deque
import cmath as cm
import numpy as np
from math import ceil

DRY_GAIN = 0
WET_GAIN = 1

class ReverbEffect(EffectPipe):
    '''
        Reverb Effect.

        TODO: Write more documentation.
    '''
    def __init__(self, rate, ch, dtype, dgain = 0.7, wgain = 0.7,
                delays=[43, 53, 61, 71], primes=True):
        '''

        Constructor

        Parameters:
            rate: Sampling rate. Default: 44100
            ch: Number of channels. Default: 2
            dtype: Numpy data type. Default: np.int16
                   [np.int16, np.int32, np.float32]
            dgain: The ratio for "Dry" gain. Default: 0.7
            wgain: The ratio for "Wet" gain. Default: 0.7
            delays: List containing the number of delays to
                    use for the early reflections. Default: [43, 53, 61, 71]
                    Note: This array must have at least one value, but should
                          optimally have 4. More than 4 might impact performance.
            primes: Makes it so that number of samples in each
                    delay to set to the next prime number greater
                    than the normal amount of samples.


        Note: Types are enforced for the default constructor arguments
              in the base class EffectPipe.

        '''
        super().__init__(rate, ch, dtype, dgain, wgain)
        next_prime = lambda a: (ceil((a-1)/6)*6)+1
        delay_times = delays
        # delay_times = [43]
        self.__ms = rate // 1000
        self.__delays = []
        for i in delay_times:
            if(primes):
                self.__delays.append(np.zeros(shape=(next_prime(i*self.__ms),ch), dtype=(self.type)))
            else:
                self.__delays.append(np.zeros(shape=(i*self.__ms,ch), dtype=(self.type)))
        self.__queue = deque()

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
        data_size = data.shape[0]
        add_data = (data * self.gain[WET_GAIN]).astype(self.type)
        out_data = np.zeros(shape=data.shape, dtype=self.type)
        for i in range(len(self.__delays)):
            if(self.__delays[i].shape[0] < data_size):
                self.__delays[i] = np.append(self.__delays[i], data[:(data_size - self.__delays[i].shape[0])], axis=0)
            a = (self.__delays[i][:data_size] * 0.7).astype(self.type)
            self.__delays[i] = np.append(self.__delays[i][data_size:], np.add(add_data, a), axis=0)
            out_data = np.add(out_data, (a*self.gain[WET_GAIN]).astype(self.type))
        return np.add(out_data, (data * self.gain[DRY_GAIN]).astype(self.type))
