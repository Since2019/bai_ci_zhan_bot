# -*-coding:utf-8-*-
import os
import re
import wave
import numpy as np
import pyaudio

# 音频比对子体时间小于母体


class Voice():
    def __init__(self):
        self.name = []  # 音频文件转码后
        self.framerate = 10
        self.nframes = 10
        self.wave_data = []

    def loaddata(self, filepath):
        if type(filepath) != str:
            print('文件的路径不正确')
            return False
        p1 = re.compile('\.wav')
        if p1.findall(filepath) is None:
            print('请确保文件的格式属于wav')
            return False
        try:
            f = wave.open(filepath, 'rb')
            print(f)
            parmas = f.getparams()
            self.nchannels, self.sampwidth, self.framerate, self.nframes = parmas[:4]
            str_data = f.readframes(self.nframes)
            self.wave_data = np.fromstring(str_data, dtype=np.short)

            return True
        except:
            print('File error!')


if __name__ == '__main__':
    p = Voice()
    # 加载具体音频路径
    p.loaddata("./correct_1.wav")
