from EffectPipe import EffectPipe
from DelayEffect import DelayEffect
from CombFilter import CombFilter
from collections import deque
import cmath as cm
import numpy as np
import AudioUtil as au


class ReverbEffect(EffectPipe):
    '''
        Reverb Effect.

        TODO: Write more documentation.
    '''
    def __init__(self, rate, ch, dtype, blocksize = 0, dgain = 0.7, wgain = 0.7):
        '''

        Constructor

        Parameters:
            rate: Sampling rate. Default: 44100
            ch: Number of channels. Default: 2
            dtype: Numpy data type. Default: np.int16
                   [np.int16, np.int32, np.float32]

        Note: Types are enforced in the base class EffectPipe

        '''
        super().__init__(rate, ch, dtype, blocksize, dgain, wgain)
        self.__queue = deque()
        self.__filters = [
                            CombFilter(rate, ch, dtype, dgain=0.7, wgain=0.7, time=23), CombFilter(rate, ch, dtype, dgain=0.7, wgain=0.7, time=37),
                            CombFilter(rate, ch, dtype, dgain=0.7, wgain=0.7, time=47), CombFilter(rate, ch, dtype, dgain=0.7, wgain=0.7, time=61),
                        ]
        #self.__last_sample = np.zeros(shape=(blocksize,ch), dtype=self.type)

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
        for i in range(4):
            self.__filters[i].push(data)

        a = au.add_samples(self.__filters[0].get(), self.__filters[1].get())
        b = au.add_samples(self.__filters[2].get(), self.__filters[3].get())
        return au.add_samples_gain(au.add_samples_gain(a, b, self.gain[1]), data, 0.7, 0.9)
        #d = au.add_samples_gain(data, c, 0.7)
