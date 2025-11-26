import soundcard as sc

from softscope.typing import AudioData
from . import BaseAudioPlayer

class SoundCardPlayer(BaseAudioPlayer):
    def __init__(self):
        self.speaker = sc.default_speaker()
        print(type(self.speaker))

    def read(self) -> AudioData:
        ...