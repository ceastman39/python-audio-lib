from collections import deque
import sounddevice as sd

class EffectPipe:
    '''
    EffectPipe:

        Abstract class for all effects to be derived from.

        TODO: Write more documentation.
    '''
    def __init__(self, rate = 44100, depth = 16, ch = 2):
        self.__RATE = rate
        self.__DEPTH = depth
        self.__CHANNELS = ch
        self.__queue = deque()

    def push(self, data):
        self.__queue.append(data)
        return

    def get(self):
        return self.__queue.popleft()
