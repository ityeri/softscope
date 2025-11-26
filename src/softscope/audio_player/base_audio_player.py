from abc import abstractmethod

from softscope.typing import AudioData


@abstractmethod
class BaseAudioPlayer:

    @abstractmethod
    def set_start(self, start_time: float | None = None): ...
    @abstractmethod
    def read(self) -> AudioData: ...