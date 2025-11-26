from abc import abstractmethod

from softscope.typing import AudioData


@abstractmethod
class BaseAudioPlayer:

    @abstractmethod
    def read(self) -> AudioData: ...