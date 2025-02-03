import numpy
import pygame
import numpy as np
from numpy.typing import NDArray

from softscope.oscilloscope_style import OscilloscopeStyle, OscilloscopeType
from softscope.typing import AudioData, SingleSample

class OscilloscopeRenderer:
    def __init__(self, surface: pygame.Surface, *,
                 surface_center: tuple[int, int] | None = None,
                 surface_radius: int | None = None,
                 scope_style: OscilloscopeStyle | None = None):

        self.surface: pygame.Surface = surface # 알파채널 Surface
        self.buffer: NDArray[NDArray[numpy.float64]] = np.empty(shape=(0, 2))

        self.surface_center_x: int = None
        self.surface_center_y: int = None
        self.surface_radius: int = None

        self.set_surface(surface,
                         surface_center=surface_center,
                         surface_radius=surface_radius)

        self.scope_style: OscilloscopeStyle

        if scope_style is None:
            self.scope_style = OscilloscopeStyle(
                type= OscilloscopeType.BASIC,
                color= (255, 255, 255, 200)
            )
        else: self.scope_style = scope_style


    def set_surface(self, surface: pygame.Surface, *,
                    surface_center: tuple[int, int] | None = None,
                    surface_radius: int | None = None):
        self.surface = surface

        if surface_center is None:
            self.surface_center_x = self.surface.get_width() / 2
            self.surface_center_y = self.surface.get_height() / 2
        else: self.surface_center_x, self.surface_center_y = surface_center

        if surface_radius is None:
            if self.surface.get_width() < self.surface.get_height():
                self.surface_radius = self.surface.get_width() / 2 * 2
            else: self.surface_radius = self.surface.get_height() / 2 * 2
        else: self.surface_radius = surface_radius



    def extend(self, data: AudioData):
        self.buffer = numpy.concatenate((self.buffer, data))

    def render(self):
        cover_surface = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)
        cover_surface.fill((0, 0, 0, 200))
        self.surface.blit(cover_surface, (0, 0))

        before_sample_index: int = 0
        current_sample_index: int = 0

        for i in range(1, int(self.buffer.shape[0] / self.scope_style.step)):
            before_sample_index = current_sample_index
            current_sample_index = int(i*self.scope_style.step)

            before_sample = self.buffer[before_sample_index]
            current_sample = self.buffer[current_sample_index]

            pygame.draw.line(self.surface, (255, 255, 255, 1),
                             self.sample_to_surface_value(before_sample),
                             self.sample_to_surface_value(current_sample))



        self.buffer = np.empty(shape=(0, 2))
        # surface_array = pygame.surfarray.array3d(self.surface)



    def sample_to_surface_value(self, sample: SingleSample) -> tuple[float, float]:
        x = float(sample[0] * self.surface_radius + self.surface_center_x)
        y = float(-sample[1] * self.surface_radius + self.surface_center_y)
        return x, y