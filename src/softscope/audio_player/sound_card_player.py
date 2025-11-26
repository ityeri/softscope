import soundcard as sc

from softscope.typing import AudioData
from . import BaseAudioPlayer

# Not implemented

class SoundCardPlayer(BaseAudioPlayer):
    def __init__(self):
        self.speaker = sc.default_speaker()
        print(type(self.speaker))

    def set_start(self, start_time: float | None = None): ...

    def read(self) -> AudioData: ...