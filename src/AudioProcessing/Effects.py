import numpy as np
from collections import deque
import warnings
from math import ceil

'''
The "Effects" module contains the "abstract" base-classes for all of the
effects, as well as some pre-made effects.
'''

# ===== Constants =====

DRY_GAIN = 0
WET_GAIN = 1

# ===== Classes =====

class EffectBase:
    '''
        Abstract class for all effects to be derived from.

        TODO: Write more documentation.
    '''
    def __init__(self, rate = 44100, ch = 2, dtype = np.int16, dgain = 0.7, wgain = 0.3):
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
    ##endregion

class DelayEffect(EffectBase):
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
              in the base class EffectBase

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

    def clear(self):
        '''

        Clears the current effect queue. Basically just calls "clear()"
        on the deque containing all of the processed samples.


        '''
        self.__queue.clear()

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

class CombFilter(EffectBase):
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

    def clear(self):
        '''

        Clears the current effect queue. Basically just calls "clear()"
        on the deque containing all of the processed samples.


        '''
        self.__queue.clear()

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

class ReverbEffect(EffectBase):
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
              in the base class EffectBase.
        '''
        super().__init__(rate, ch, dtype, dgain, wgain)
        # Turns a number 'a' into the next highest prime number.
        next_prime = lambda a: (ceil((a-1)/6)*6)+1
        # delay_times = [43]
        self.__ms = rate // 1000
        self.__comb_delays = []
        self.__queue = deque()

        for i in delays:
            if(primes):
                self.__comb_delays.append(np.zeros(shape=(next_prime(int(i)*self.__ms),ch), dtype=(self.type)))
            else:
                self.__comb_delays.append(np.zeros(shape=(int(i)*self.__ms,ch), dtype=(self.type)))


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

    def clear(self):
        '''

        Clears the current effect queue. Basically just calls "clear()"
        on the deque containing all of the processed samples.


        '''
        self.__queue.clear()

    def __add_effect(self, data):
        '''

        The function that modifies the data as it's being pushed.

        Parameters:
            data: numpy array containing audio data.

        '''
        data_size = data.shape[0]
        add_data = (data * self.gain[WET_GAIN]).astype(self.type)
        out_data = np.zeros(shape=data.shape, dtype=self.type)
        for i in range(len(self.__comb_delays)):
            if(self.__comb_delays[i].shape[0] < data_size):
                self.__comb_delays[i] = np.append(self.__comb_delays[i], data[:(data_size - self.__comb_delays[i].shape[0])], axis=0)
            a = (self.__comb_delays[i][:data_size] * 0.7).astype(self.type)
            self.__comb_delays[i] = np.append(self.__comb_delays[i][data_size:], np.add(add_data, a), axis=0)
            out_data = np.add(out_data, (a*self.gain[WET_GAIN]).astype(self.type))
        return np.add(out_data, (data * self.gain[DRY_GAIN]).astype(self.type))
