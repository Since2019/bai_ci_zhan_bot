from .two_audio_files_cmp_test import *

# 用来读取音频文件
from scipy.io.wavfile import read
import os

INT_DIFFERENCE_THRESHOLD = 500


def check_correct(target_sample, correct_sample_source=None):
    '''
        Passes in two .wav files
    '''
    samprate, target_sample = read(target_sample)

    print('targett_sample, tuple object, no flatten()?')
    print(type(target_sample))
    print(target_sample)

    if correct_sample_source is None:
        samprate2, correct_sample_source = read(
            os.path.dirname(__file__)+'/correct.wav')

    # 看看是否播报为“正确”
    try:
        retval1, retval2,  difference_after_alignment = align_volume(
            target_sample, correct_sample_source)

        # 高于 INT_DIFFERENCE_THRESHOLD 的就是不一样的
        if(np.abs(difference_after_alignment) > INT_DIFFERENCE_THRESHOLD):
            __debug__ and print(
                "The two samples are not similar to each other")
        else:
            __debug__ and print('Correct !!!!!!!!')
            return True
    except Exception:
        pass

    return False


def check_wrong(target_sample, wrong_sample_source=None):
    '''
        Passes in two .wav files
    '''
    samprate, target_sample = read(target_sample)

    print(type(target_sample))
    print(target_sample)

    if wrong_sample_source is None:
        samprate2, wrong_sample_source = read(
            os.path.dirname(__file__)+'/wrong.wav')

    try:
        # 看看是否播报为“错误”
        retval1, retval2,  difference_after_alignment = align_volume(
            target_sample, wrong_sample_source)

        # 高于 INT_DIFFERENCE_THRESHOLD 的就是不一样的
        if(np.abs(difference_after_alignment) > INT_DIFFERENCE_THRESHOLD):
            __debug__ and print(
                "The two samples are not similar to each other")
        else:
            __debug__ and print('Wrong !!!!!!!!')
            return True
    except Exception:
        pass

    return False
