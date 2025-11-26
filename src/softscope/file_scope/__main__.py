import argparse
import time
import pygame

import softscope
from softscope.oscilloscope_style import OscilloscopeStyle, OscilloscopeType
from softscope import audio_player


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='path of target audio file')
    parser.add_argument('-f', '--fps', help='frame per second', nargs='?', default='120')

    args = parser.parse_args()

    pygame.init()

    on = True
    screen_width, screen_height = 500, 500
    fps = int(args.fps)
    dt = 1000 // fps
    clk = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    scope_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    scope_renderer = softscope.OscilloscopeRenderer(
        scope_surface,
        scope_style=
        OscilloscopeStyle(
            OscilloscopeType.BASIC,
            (50, 255, 255, 127)
        )
    )

    file_path = args.file

    sound = pygame.mixer.Sound(file_path)
    audio_player = audio_player.AudioFilePlayer(file_path)

    fps_timer = time.time() + 1

    audio_player.set_start()
    sound.play()

    while on:
        dt = clk.tick(fps)

        if fps_timer <= time.time():
            fps_timer = time.time() + 1
            print(f'{clk.get_fps()} fps')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False
            elif event.type == pygame.VIDEORESIZE:
                screen_size = screen.get_size()

                scope_surface = pygame.Surface(screen_size, pygame.SRCALPHA)
                scope_renderer.set_surface(scope_surface)

        screen.fill((0, 12, 0, 255))

        scope_renderer.extend_sample(
            audio_player.read(1500)
        )

        scope_renderer.render()
        screen.blit(
            scope_surface, (0, 0)
        )

        pygame.display.flip()