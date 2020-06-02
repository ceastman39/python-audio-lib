import numpy as np
import cmath as cm
'''

Utility functions to be used when manipulating audio data.

'''

def add_samples(x, y):
    '''

    Adds two audio data samples.

    TODO: Add clipping prevention.

    Parameters:
        x: Numpy array to add to.
        y: Numpy array to add from.

    '''
    return np.add(x, y)

def add_samples_gain(x, y, xgain, ygain = None):
    '''

    Multiplies two samples by a certain gain ration,
    and then adds the resulting two audio data samples.

    TODO: Add clipping prevention.

    Parameters:
        x: Numpy array to add to.
        y: Numpy array to add from.
        xgain: Float value to multiply with x.
        ygain, Optional: Float value to multiply with y. If none given,
                         then it will be the same value as xgain.

    '''
    if(ygain == None): ygain = xgain
    tx, ty = x.dtype, y.dtype
    return np.add(np.multiply(x, xgain, casting="unsafe", dtype=tx), np.multiply(y, ygain, casting="unsafe", dtype=ty))

def phase_shift_90(data):
    '''

    Shifts the phase of the given sample by 90 degrees.

    TODO: Add clipping prevention.

    Parameters:
        data: Audio sample to shift.

    '''
    t = data.dtype
    new_data = np.fft.rfft(data, 1) * cm.rect(1., np.pi/2)
    d = np.fft.irfft(new_data, 1).astype(t)
    print(d)
    return d
