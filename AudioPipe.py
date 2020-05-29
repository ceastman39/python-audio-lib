

class AudioPipe:
    '''
    AudioPipe:

    A base class for all audio pipelines. Contains the buffer for the audio
    data. Does no safety checking on the data being queued, and any derived
    class should ensure all data is valid.

    TODO: Write more documentation...
    '''
    def __init__(self):
        self.__buffer = deque()


    def _push(self, data):
        self.__buffer.append(data)
        return

    def _dequeue(self):
        return self.__buffer.popleft()
