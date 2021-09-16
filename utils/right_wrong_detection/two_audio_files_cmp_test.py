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

INT_DIFFERENCE_THRESHOLD = 500


def remove_silence(wav_data):
    # print('np.array([0, 0])')
    # print(np.array([0, 0]))

    # idx = np.argwhere(np.all(wav_data[..., :] == np.array([0, 0])))

    # print('wav_data[0]')
    # print(wav_data[0])

    # print('idx')
    # print(idx)

    # new_wav_data = np.delete(wav_data, idx, axis=1)

    new_wav_data = []
    for item in wav_data:
        if(np.all(np.abs(item) <= 1000)):
            # if(np.all(item <= 1000)):
            # print("零")
            pass
        else:
            # print(item)
            if(item.size == 2):
                item = max(item)
                # print(item)
            new_wav_data.append(item)

            # print(item)
            # print("非零")
            pass

    retval = np.array(new_wav_data)
    return retval


def check_std_diviation(wav1=None, wav2=None):
    diff = 0
    wavdata = []
    wavdata_target = []

    if(not wav1.any()):
        pass
    else:
        wavdata = wav1

    if(not wav2.any()):
        pass
    else:
        wavdata_target = wav2

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
            return np.sum(diff)
        else:
            # print(chunk - wavdata_target[idx])
            diff += chunk - wavdata_target[idx]
            print()
    return diff


def test_silence(wav_data):
    for item in wav_data:
        if(np.all(item == 0)):
            # print("零")
            pass

        else:
            pass
            print("非零")


def to_frequency_domain(wav_data):

    freq_domain = fft(wav_data)
    # print('type(freq_domain)')
    # print(type(freq_domain))

    # print('freq_domain')
    # print(freq_domain)
    return freq_domain


def convert_frames_to_fft():
    samprate, wavdata = read('./correct_1.wav')
    samprate_target, target_wavdata = read('./correct_3.wav')

    wavdata = remove_silence(wavdata)
    target_wavdata = remove_silence(target_wavdata)

    chunk_size = 1
    target_chunk_size = 1

    chunks = np.array_split(wavdata, chunk_size)
    target_chunks = np.array_split(target_wavdata, target_chunk_size)

    for idx, chunk in enumerate(chunks):

        # print(idx)

        dft = fft(chunk)
        dft_target = fft(target_chunks[idx])
        # print(stats.ks_2samp(dft.flatten(), dft_target.flatten()))
        # print(stats.ks_2samp(dft, dft_target))
        # print(stats.ks_2samp(chunk, target_chunks[idx]))

        chunk_norm = np.linalg.norm(chunk)
        target_chunks_norm = np.linalg.norm(target_chunks[idx])
        print(stats.ks_2samp(chunk_norm.flatten(), target_chunks_norm.flatten()))

        # # normalize before ks-test
        # dft_norm = np.linalg.norm(dft)
        # dft_target_norm = np.linalg.norm(dft_target)
        # print(stats.ks_2samp(dft_norm.flatten(), dft_target_norm.flatten()))


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

        # 如果其中较短的那个即将装满
        if(idx == (len_shorter - 1)):
            # 把差之和加起来
            return np.sum(diffs), diffs

        # 如果短的和长的都依然够长
        else:
            diffs.append(
                int((chunk - wavdata_target[idx]) / 100))


def find_highest(wav_data):
    ''' finds the highest volume in the wav_data
        and returns an integer
        param  : {wav_data} - datatype: numpy array  
        retval : {max_val}  - maximum value of the 
    '''
    __debug__ and print('looking for the biggest value in this wav file...')

    flattened = wav_data.flatten()
    max_val = max(flattened)

    __debug__ and print(f'max_val: {max_val}')

    return max_val


def align_volume(wav_data_one, wav_data_two):
    # 先对齐(降噪后，声音最大值对齐)
    print('align_volume')

    vol_one_peak = find_highest(wav_data_one)
    vol_two_peak = find_highest(wav_data_two)

    peaks = {vol_one_peak: 'vol_one_peak',
             vol_two_peak: 'vol_two_peak'
             }

    # 获取更大的那个的名字
    higher_peak_wav = peaks.get(max(peaks))

    highest_vol = max(vol_one_peak, vol_two_peak)

    vol_one_aligned = remove_silence(wav_data_one)
    vol_two_aligned = remove_silence(wav_data_two)

    # print('higher_peak_wav')
    # print(higher_peak_wav)

    # 会损耗数据
    if(higher_peak_wav == 'vol_one_peak'):
        # 1 比 2 高：
        vol_one_aligned = vol_one_aligned
        vol_two_aligned = vol_two_aligned * (highest_vol / vol_two_peak)
    elif(higher_peak_wav == 'vol_two_peak'):
        # 2 比 1 高：
        vol_one_aligned = vol_one_aligned * (highest_vol / vol_two_peak)
        vol_two_aligned = vol_two_aligned

    # vol_one_aligned = wav_data_one / vol_one_peak * highest_vol
    # vol_two_aligned = wav_data_two / vol_two_peak * highest_vol

    # find_highest(vol_one_aligned)
    # find_highest(vol_two_aligned)

    print(remove_silence(vol_one_aligned))
    print(remove_silence(vol_two_aligned))

    difference_after_alignment = None
    try:
        difference_after_alignment, retval2 = check_difference(
            vol_one_aligned, vol_two_aligned)
        print("difference after aligning vol:")
        print(difference_after_alignment)
        return vol_one_aligned, vol_two_aligned, difference_after_alignment

    except Exception:
        pass


# if __name__ == '__main__':

#     file_name_1 = "output.wav"
#     file_name_2 = "correct.wav"

#     samprate, wavdata = read(file_name_1)
#     samprate_target, wavdata_target = read(file_name_2)

#     retval1, retval2 = check_difference(wavdata, wavdata_target)

#     # 两个音频的差值
#     print("difference:")
#     print(retval1)

#     plt.figure(0)
#     plt.title("retval2")
#     # plt.plot(fft(retval2))
#     plt.plot(retval2)

#     freq_diff = fft(retval2)
#     pdata = np.angle(freq_diff)  # phase
#     plt.figure(1)
#     plt.title("pdata")
#     plt.plot(pdata)

#     spf = wave.open(file_name_1, "r")
#     spf2 = wave.open(file_name_2, "r")

#     # 先对齐(降噪后，声音最大值对齐)
#     signal, signal2, difference_after_alignment = align_volume(
#         wavdata, wavdata_target)

#     if(np.abs(difference_after_alignment) > INT_DIFFERENCE_THRESHOLD):
#         print("You are comparing correct against wrong")
#     else:
#         print("both are the same correct/wrong sfx")

#     # Extract Raw Audio from Wav File
#     signal = spf.readframes(-1)
#     signal = np.fromstring(signal, "Int16")
#     signal = remove_silence(signal)

#     # Extract Raw Audio from Wav File
#     signal2 = spf2.readframes(-1)
#     signal2 = np.fromstring(signal2, "Int16")
#     signal2 = remove_silence(signal2)
#     # # If Stereo
#     # if spf.getnchannels() == 2:
#     #     print("Just mono files")
#     #     sys.exit(0)

#     plt.figure(3)
#     plt.title(f"File: {file_name_1}")
#     plt.plot(signal)
#     # plt.plot(fft(signal))
#     # plt.show()

#     # # If Stereo
#     # if spf2.getnchannels() == 2:
#     #     print("Just mono files")
#     #     sys.exit(0)

#     plt.figure(5)
#     plt.title(f"File: {file_name_2}")
#     plt.plot(signal2)
#     # plt.plot(fft(signal2))

#     # plt.figure(3)
#     # plt.title("difference")
#     # plt.plot(signal - signal2)

#     # 显示图像
#     plt.show()

#     convert_frames_to_fft()

#     # find_highest(wavdata)
#     # find_highest(wavdata_target)
