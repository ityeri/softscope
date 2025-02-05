import numpy as np
import pyaudio

from softscope.typing import AudioData
from softscope.base_audio_manager import BaseAudioManager

p = pyaudio.PyAudio()

class LiveMicManager(BaseAudioManager):
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


    def read(self) -> AudioData:
        data = self.stream.read(self.chunk_size)

        raw_audio_data = np.frombuffer(data, dtype=np.float32)

        stereo_audio_data = np.reshape(raw_audio_data, (-1, 2))

        return stereo_audio_data



    @classmethod
    def check_available_device(cls, check_out_device: bool = False):
        print("사용 가능한 모든 녹음 장치:")
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            # 입력 장치만 출력
            if device_info["maxInputChannels"] > 0:
                print(f" |  디바이스 번호: {i}, 이름: {device_info['name']}, "
                      f"입력 채널 수: {device_info['maxInputChannels']}, "
                      f"기본 샘플링 레이트: {device_info['defaultSampleRate']}")

        if check_out_device:

            print("\n===\n")
            print("사용 가능한 모든 재생 장치:")
            for i in range(p.get_device_count()):
                device_info = p.get_device_info_by_index(i)
                # 입력 장치만 출력
                if device_info["maxOutputChannels"] > 0:
                    print(f" |  디바이스 번호: {i}, 이름: {device_info['name']}, 출력 체널 수: {device_info['maxOutputChannels']}")