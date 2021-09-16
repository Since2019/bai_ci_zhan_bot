"""PyAudio example: Record a few seconds of audio and save to a WAVE file.
   检测系统声音是否大于5分贝，高于5dB的时候进行录音。
   如果

"""
import datetime

import pyaudio
import wave

import statistics
import numpy as np
import math

import time

import os

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"
CHUNK_SIZE = int(RATE/2)

# Decibels
ZERO_DECIBEL = int(0)

# 录音

TEMP_FOLDER_PATH = os.path.join(os.path.dirname(__file__),  'WAV_TEMP',)


def record_wav():
    print("=========== in record_wav() =====================")
    noise = True
    bool_started = False
    ended = False

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=1)

    print("* recording")

    frames = []

    while True:

        chunk = stream.read(int(CHUNK))  # 读取输入流
        result = np.fromstring(chunk, dtype=np.int16)  # bytes 转换成numpy array

        # print(result)
        if(result.any()):
            # 如果有声音：
            if check_decibels(result) > 20:
                # 还没有开始的话，标记为开始
                if(bool_started == False):
                    bool_started = True

                # __debug__ and print('有声音')
                frames.append(chunk)

            # 如果超静音
            elif(check_decibels(result) < 20):
                # 开始过了，现在就结束。
                if(bool_started == True):
                    break
                else:
                    pass

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')

    if not os.path.isdir(TEMP_FOLDER_PATH):
        os.mkdir(TEMP_FOLDER_PATH)

    # print(WAVE_OUTPUT_FILENAME)
    # print(TEMP_FOLDER_PATH)
    # print(TEMP_FOLDER_PATH + time_now + '.wav')

    wf2 = wave.open(os.path.join(TEMP_FOLDER_PATH, time_now + '.wav'), 'wb')

    wf2.setnchannels(CHANNELS)
    wf2.setsampwidth(p.get_sample_size(FORMAT))
    wf2.setframerate(RATE)
    wf2.writeframes(b''.join(frames))
    wf2.close()

    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def check_decibels(chunk):
    # print(len(chunk))

    # ck = np.ndarray((CHUNK_SIZE, 1), np.float64, chunk)
    # print(chunk)

    chunk_abs = np.abs(chunk)**2

    try:
        db = 20*np.log10(np.sqrt(statistics.mean((chunk_abs).flatten())))
        # print("db:")
        # print(db)

        if(db == float('-inf')):
            # __debug__ and print('无声音')
            return 0
        else:
            return db

    except Exception:
        print(Exception)
        pass

    return 0


if __name__ == '__main__':
    # while True:
    record_wav()
