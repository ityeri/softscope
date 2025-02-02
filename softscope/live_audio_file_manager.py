import time
from io import FileIO

import soundfile

from softscope.typing import AudioData


class LiveAudioFileManager:
    def __init__(self, file: str | FileIO):

        file_data = soundfile.read(file)

        self.audio_data: AudioData = file_data[0]
        self.sample_rate: int = file_data[1]

        self.start_time: float = time.time()

    def set_start(self) -> None: self.start_time = time.time()

    def time_to_sample_index(self, time_sec: float) -> int: return int(time_sec * self.sample_rate)

    def get_current_time(self) -> float: return time.time() - self.start_time
    def get_current_sample_index(self) -> int: return self.time_to_sample_index(self.get_current_time())



    def get_current_audio_data(self, sample_count: int) -> AudioData:
        current_sample_index = self.get_current_sample_index()

        start_index = current_sample_index - sample_count
        if start_index < 0: start_index = 0

        current_audio_data = self.audio_data[start_index : current_sample_index]

        return current_audio_data