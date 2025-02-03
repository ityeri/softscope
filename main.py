import time

import pygame

import softscope



# pygame 기본 세팅
pygame.init()

on = True
screen_size = (500, 500)
fps = 120
dt = 1000 // fps
clk = pygame.time.Clock()

screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)



# OscilloscopeRenderer 세팅
scope_surface = pygame.Surface(screen_size, pygame.SRCALPHA)
scope_renderer = softscope.OscilloscopeRenderer(scope_surface)

# 파일 불러오기
file_path = "sample/sirius.mp3"

sound = pygame.mixer.Sound(file_path)
live_audio_file_manager = softscope.LiveAudioFileManager(file_path)



# fps 모니터링 설정
timer = time.time() + 1


# 메인 코드
live_audio_file_manager.set_start()
sound.play()

while on:
    dt = clk.tick(fps)

    if timer <= time.time():
        timer = time.time() + 1
        print(clk.get_fps())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            on = False
        elif event.type == pygame.VIDEORESIZE:
            screen_size = screen.get_size()

            scope_surface = pygame.Surface(screen_size, pygame.SRCALPHA)
            scope_renderer.set_surface(scope_surface)

    screen.fill((0, 12, 0, 255))



    scope_renderer.extend(
        live_audio_file_manager.get_current_audio_data(1000)
    )

    scope_renderer.render()
    screen.blit(
        scope_surface, (0, 0)
    )



    pygame.display.flip()