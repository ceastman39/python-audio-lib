from EffectPipe import EffectPipe
from collections import deque
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
            time: Delay in milliseconds. Default: 500

        Note: Types are enforced in the base class EffectPipe

        '''
        super().__init__(rate, ch, dtype)
        self.__queue = deque()
        self.__delay_queues = [deque(np.zeros((time*(rate//1000)), dtype=self.type)) for i in range(ch)]

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
            for j in range(self.channels):
                self.__delay_queues[j].append(data[i][j])
                effect_data[i][j] = self.__delay_queues[j].popleft()
        return au.add_samples(data, effect_data)
