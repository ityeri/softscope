import time
from io import FileIO

import soundfile

from . import BaseAudioPlayer
from softscope.typing import AudioData


class AudioFilePlayer(BaseAudioPlayer):
    def __init__(self, file: str | FileIO):

        file_data = soundfile.read(file)

        self.audio_data: AudioData = file_data[0]
        self.sample_rate: int = file_data[1]

        self.start_time: float = time.time()

        self.played_time_old: float = 0

    def set_start(self) -> None: self.start_time = time.time()

    def time_to_sample_index(self, time_sec: float) -> int: return int(time_sec * self.sample_rate)

    def get_played_time(self) -> float: return time.time() - self.start_time



    def read(self, sample_count: int) -> AudioData: # TODO
        start_index = self.time_to_sample_index(self.played_time_old)

        current_played_time = self.get_played_time()
        current_sample_index = self.time_to_sample_index(current_played_time)

        # if start_index < 0: start_index = 0

        current_audio_data = self.audio_data[start_index : current_sample_index]

        self.played_time_old = current_played_time

        return current_audio_data