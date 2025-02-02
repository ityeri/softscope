import time

import pygame
import soundfile

import softscope



# pygame 기본 세팅
pygame.init()

on = True
screen_size = (700, 700)
fps = 120
dt = 1000 // fps
clk = pygame.time.Clock()

screen = pygame.display.set_mode((700, 700))



# OscilloscopeRenderer 세팅
scope_surface = pygame.Surface((700, 700))
scope_renderer = softscope.OscilloscopeRenderer(scope_surface, (350, 350), 350)

# 파일 불러오기
file_path = "sample/sirius.mp3"

sound = pygame.mixer.Sound(file_path)
live_audio_file_manager = softscope.LiveAudioFileManager(file_path)



# 메인 코드
live_audio_file_manager.set_start()
sound.play()

while on:
    dt = clk.tick(fps)
    screen_size = screen.get_size()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: on = False

    screen.fill((0, 0, 0))


    # print(live_audio_file_manager.get_current_sample_index())

    scope_renderer.extend(
        live_audio_file_manager.get_current_audio_data(1000)
    )

    scope_renderer.render()
    screen.blit(
        pygame.transform.scale(scope_surface, screen_size), (0, 0)
    )



    pygame.display.flip()