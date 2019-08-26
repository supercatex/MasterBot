import pyaudio
import numpy as np
import wave
import matplotlib.pyplot as plt
from scipy.io import wavfile
from playsound import playsound
from pylab import *


class AudioManager(object):

    def __init__(self):
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 2
        self.frame_rate = 44100

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.frame_rate,
            input=True,
            frames_per_buffer=self.chunk
        )

    def start_recoding(self, thresh=5000):
        print("* start recoding *")
        state = 0
        count = 0
        begin = 0
        frames = np.array([])
        while state != 2:
            data = self.stream.read(self.chunk)
            temp = np.fromstring(data, dtype=np.int16)
            if len(np.where(np.abs(temp) > thresh)[0]) > 0:
                if state == 0:
                    state = 1
                    begin = (len(frames) + np.where(np.abs(temp) > thresh)[0][0]) // self.channels
                    begin -= int(self.frame_rate * 0.25)
                    begin = np.max(begin, 0)
                    begin -= begin % self.chunk
                count = 0
            else:
                count += 1
                if state == 1 and count > self.frame_rate // self.chunk * 0.5:
                    state = 2
            frames = np.append(frames, temp)
            for t in temp:
                print("\r" + str(t), end="")
        print()
        print("* end recoding *")
        frames = frames.reshape((-1, self.channels))
        return frames[begin:]

    def show_graph(self, frames):
        timing = np.linspace(0, len(frames) // self.frame_rate, num=len(frames))

        if len(frames.shape) == 1:
            plt.figure(figsize=(8, 6))
            plt.title('Audio Graph')
            plt.plot(timing, frames / np.iinfo(np.int16).max, '-', linewidth=1, color="c")
            plt.xlabel('time (seconds)')
            plt.ylabel('Bit Depth - 16bits')
            plt.ylim(-1, 1)
            thismanager = get_current_fig_manager()
            thismanager.window.wm_geometry("+0+0")
        else:
            plt.figure(figsize=(12, 6))
            plt.subplot(2, 1, 1)
            plt.title('Audio Graph')
            plt.plot(timing, frames[:, 0] / np.iinfo(np.int16).max, '-', linewidth=1, color="m")
            plt.ylabel('LEFT Bit Depth - 16bits')
            plt.ylim(-1, 1)

            plt.subplot(2, 1, 2)
            plt.plot(timing, frames[:, 1] / np.iinfo(np.int16).max, '-', linewidth=1, color="c")
            plt.xlabel('time (seconds)')
            plt.ylabel('RIGHT Bit Depth - 16bits')
            plt.ylim(-1, 1)
            thismanager = get_current_fig_manager()
            thismanager.window.wm_geometry("+50+100")

        plt.show()

    def save_audio(self, file, frames):
        wf = wave.open(file, "wb")
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.format))
        wf.setframerate(self.frame_rate)
        wf.writeframes(np.int16(frames))
        wf.close()

    def read_audio(self, file):
        fs, data = wavfile.read(file)
        return fs, data

    def play_audio(self, file):
        playsound(file)


if __name__ == "__main__":
    _am = AudioManager()

    _frames = _am.start_recoding()
    _am.save_audio("temp.wav", _frames)
    _am.play_audio("temp.wav")
    _am.show_graph(_frames)

    # _file = "../datasets/sounds/train/audio/happy/2e0d80f7_nohash_0.wav"
    # _fs, _frames = _am.read_audio(_file)
    # _am.frame_rate = _fs
    # _am.play_audio(_file)
    # _am.show_graph(_frames)
