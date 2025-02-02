import numpy
import pygame
import numpy as np
from numpy.typing import NDArray
from softscope.typing import AudioData, SingleSample

class OscilloscopeRenderer:
    def __init__(self, surface: pygame.Surface, surface_center: tuple[int, int], surface_radius: int):
        self.surface: pygame.Surface = surface # 알파채널 Surface
        self.buffer: NDArray[NDArray[numpy.float64]] = np.empty(shape=(0, 2))

        self.surface_center_x: int = surface_center[0]
        self.surface_center_y: int = surface_center[1]
        self.surface_radius: int = surface_radius



    def extend(self, data: AudioData):
        self.buffer = numpy.concatenate((self.buffer, data))

    def render(self):
        self.surface.fill((0, 0, 0, 0))



        for i, sample_index in enumerate(self.buffer[1:]):
            before_sample = self.buffer[i - 1]
            current_sample = self.buffer[i]

            pygame.draw.line(self.surface, (255, 0, 0, 30),
                             self.sample_to_surface_value(before_sample),
                             self.sample_to_surface_value(current_sample))



        self.buffer = np.empty(shape=(0, 2))
        # surface_array = pygame.surfarray.array3d(self.surface)



    def sample_to_surface_value(self, sample: SingleSample) -> tuple[float, float]:
        x = float(sample[0] * self.surface_radius + self.surface_center_x)
        y = float(-sample[1] * self.surface_radius + self.surface_center_y)
        return x, y