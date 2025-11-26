import math

import numpy
import pygame
import numpy as np

from softscope.oscilloscope_style import OscilloscopeStyle, OscilloscopeType
from softscope.typing import AudioData, SingleSample

class OscilloscopeRenderer:
    def __init__(self, surface: pygame.Surface, *,
                 surface_center: tuple[int, int] | None = None,
                 surface_radius: int | None = None,
                 graph_amplify: float = 1,

                 style: OscilloscopeStyle | None = None,
                 graph_step: float = 1):

        self.surface: pygame.Surface = surface # 알파채널 Surface
        self.buffer: AudioData = np.empty(shape=(0, 2))

        self.surface_center_x: int = None
        self.surface_center_y: int = None

        self.surface_radius: int = None
        self.graph_amplify: float = graph_amplify
        self.graph_step: float = graph_step

        self.set_surface(
            surface,
            surface_center=surface_center,
           surface_radius=surface_radius
        )

        self.scope_style: OscilloscopeStyle

        if style is None:
            self.style = OscilloscopeStyle(
                type= OscilloscopeType.BASIC,
                color= (255, 255, 255, 127)
            )
        else: self.style = style


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
                self.surface_radius = self.surface.get_width() / 2
            else: self.surface_radius = self.surface.get_height() / 2
        else: self.surface_radius = surface_radius


    def extend_sample(self, data: AudioData):
        self.buffer = numpy.concatenate((self.buffer, data))

    def render(self):
        cover_surface = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)
        cover_surface.fill((0, 0, 0, 100))
        self.surface.blit(cover_surface, (0, 0))

        drawing_surface = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)

        before_sample_index: int = 0
        current_sample_index: int = 0

        for i in range(1, int(self.buffer.shape[0] / self.graph_step)):
            before_sample_index = current_sample_index
            current_sample_index = int(i*self.graph_step)

            before_sample = self.buffer[before_sample_index]
            current_sample = self.buffer[current_sample_index]

            before_position = self.sample_to_surface_value(before_sample)
            current_position = self.sample_to_surface_value(current_sample)

            distance = math.sqrt(
                math.pow(current_position[0] - before_position[0], 2)
                + math.pow(current_position[1] - before_position[1], 2)
            )

            color: tuple[int, int, int, int] = (255, 0, 0, 255)

            if self.style.type == OscilloscopeType.BASIC:
                color = self.style.color
            elif self.style.type == OscilloscopeType.BASIC_LIGHTING:
                attenuation_rate = (distance / self.surface_radius) * 7
                if attenuation_rate < 1:
                    attenuation_rate = 1
                color = tuple(map(lambda x: x / attenuation_rate, self.style.color))

            pygame.draw.line(
                drawing_surface, color,
                before_position,
                current_position
            )

        self.surface.blit(drawing_surface, (0, 0))

        self.buffer = np.empty(shape=(0, 2))

    def sample_to_surface_value(self, sample: SingleSample) -> tuple[float, float]:
        x = float(sample[0] * self.surface_radius * self.graph_amplify  +  self.surface_center_x)
        y = float(-sample[1] * self.surface_radius * self.graph_amplify  +  self.surface_center_y)
        return x, y