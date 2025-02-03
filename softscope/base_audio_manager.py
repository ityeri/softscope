from abc import abstractmethod

from softscope.typing import AudioData


@abstractmethod
class BaseAudioManager:

    @abstractmethod
    def read(self) -> AudioData: ...