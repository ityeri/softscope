import pygame
import numpy as np

# pygame 기본 세팅
pygame.init()

on = True
screen_size = (500, 500)
fps = 120
dt = 1000 // fps
clk = pygame.time.Clock()

screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

# 밝기가 0 ~ 0.5 사이일때는, 알파값만 조정함
# 밝기가 0.5 일때는 라이팅한 컬러가 원래 컬러와 같음 (알파값도)
# 밝기가 0.5 ~ 1 일때는 RGBA 채널이 원래 값 ~ 최대 값 까지 균일하게 증가함

def light_color(color: tuple[int, int, int, int], brightness: float) -> tuple[int, int, int, int]:
    color: np.ndarray = np.ndarray(color, np.float32)

    if 0 <= brightness <= 0.5:
        color *= brightness * 2
    elif 0.5 < brightness:
        flip_color = 1 - color
        color += flip_color * (brightness - 0.5) * 2

    return tuple(color * 255)


while on:
    dt = clk.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            on = False

    screen.fill((0, 0, 0))

    pygame.display.flip()