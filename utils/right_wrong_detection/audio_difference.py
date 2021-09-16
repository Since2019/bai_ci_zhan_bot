from os import remove
import statistics
import math
import numpy as np
from numpy.lib.function_base import diff
from scipy.io.wavfile import read

from scipy.fft import fft, ifft
from scipy import stats

import matplotlib.pyplot as plt
import numpy as np
import wave
import sys


# 去除前后超静音干扰部分
def remove_silence(wav_data):
    new_wav_data = []
    for item in wav_data:

        if(np.all(np.abs(item) <= 1000)):
            # print("零")
            pass

        else:
            if(item.size == 2):
                item = max(item)

            new_wav_data.append(item)
            pass

    retval = np.array(new_wav_data)
    return retval


# 做差，看返回的值是多少，判断相似度
def check_difference(wav1=None, wav2=None):
    print('drawing figure 0 ')
    diffs = []
    wavdata = []
    wavdata_target = []

    if(not wav1.any()):
        pass
    else:
        wavdata = remove_silence(wav1)

    if(not wav2.any()):
        pass
    else:
        wavdata_target = remove_silence(wav2)

    len1 = len(wavdata)
    len2 = len(wavdata_target)
    len_shorter = 0

    if(len1 > len2):
        len_shorter = len2
    else:
        len_shorter = len1
    # print(len_shorter)

    for idx, chunk in enumerate(wavdata):
        # print(idx)
        # print(len_shorter)
        if(idx == (len_shorter - 1)):
            # print('diff::::')
            # print(diffs)
            return np.sum(diffs), diffs

        else:
            # print(diffs)
            # print(chunk - wavdata_target[idx])
            diffs.append(int((chunk - wavdata_target[idx]) / 100))


def find_highest(wav_data):
    ''' find highest volume:'''
    print('looking for the biggest value in this wav file...')
    flattened = wav_data.flatten()
    max_val = max(flattened)
    print('max_val')
    print(max_val)
