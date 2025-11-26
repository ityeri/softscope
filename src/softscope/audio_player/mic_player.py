import numpy as np
import pyaudio

from softscope.typing import AudioData
from . import BaseAudioPlayer

p = pyaudio.PyAudio()

class MicPlayer(BaseAudioPlayer):
    def __init__(self, device_num: int, buffer_size: int = 1024, sample_late: int = 44100):
        self.stream: pyaudio.Stream = p.open(
            format=pyaudio.paFloat32,
            channels=2,
            rate=sample_late,
            input=True,
            input_device_index=device_num,
            frames_per_buffer=buffer_size
        )
        self.chunk_size: int = buffer_size

    def set_start(self, start_time: float | None = None): pass

    def read(self) -> AudioData:
        data = self.stream.read(self.chunk_size)

        raw_audio_data = np.frombuffer(data, dtype=np.float32)

        stereo_audio_data = np.reshape(raw_audio_data, (-1, 2))

        return stereo_audio_data