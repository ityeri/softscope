import soundfile as sf
import numpy as np
import time
import pygame
# from itWorkSpace import filePathUI

# TODO: 실시간 설정 조정기 만들기, 그 뭐냐그그그그 실제 fps 에 따른 배경 투명도 변경

# Pygame 초기화
pygame.init()
pygame.mixer.init()


# filePath = filePathUI("오디오 파일을 골라주세요", "오디오 파일", "mp3 wav ogg m4a", "r")

filePath = "みきとP-『-ロキ-』-MV.mp3"

def secToSample(secTime: float, smapleLate: int) -> int:
    return int(secTime * sampleLate)

def distance(point1, point2):
    point1 = np.array(point1)
    point2 = np.array(point2)
    return np.linalg.norm(point1 - point2)




# 사운드 불러오기
pygame.mixer.music.load(filePath)
audiData, sampleLate = sf.read(filePath)

# 파이썬 세팅
screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
clk = pygame.time.Clock()
fps = 120
osiloscopeSurface = pygame.Surface(pygame.display.get_window_size(), pygame.SRCALPHA)

# fps 표시할 타이머 세팅
timerInterval = 1
goalTime = time.time() + timerInterval

# 시각화 설정값들
downAlphaPerPrameRatio = 1 # 현재 프레임이 이전 프레임을 어느정도의 불투명도로 덮어 씌울건지 설정 (0 ~ 1)
osiloscopeRadius = 250 # 시각화가 보여질 화면상의 크기
lineLength = 2000 # 샘플기준 선의 길이
lineStep = 1 # 샘플 기준 선의 점 단위
lineColor = (255, 99, 85)
minLineBrightness = 0.4 # 선의 최소 밝기 (보기엔 선의 밝기와 같음)


# 타이머 시작 / 사운드 재생
startTime = time.time()-(200/1000)
pygame.mixer.music.play()

on = True

while on:
    dt = clk.tick(fps)
    
    if goalTime < time.time():
        goalTime += timerInterval
        print(f"프레임: {clk.get_fps()}    dt: {dt}")

    screen.fill((0, 0, 0))

    screenSize = pygame.display.get_window_size()
    screenCenter = (screenSize[0]/2, screenSize[1]/2)
    if screenSize[0] < screenSize[1]:
        osiloscopeRadius = screenSize[0]/2
    else:
        osiloscopeRadius = screenSize[1]/2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            on = False
        if event.type == pygame.VIDEORESIZE:
            osiloscopeSurface = pygame.Surface(pygame.display.get_window_size(), pygame.SRCALPHA)




    osiloscopeSurface.fill((0, 0, 0, 255 * downAlphaPerPrameRatio))



    playTime = time.time() - startTime
    sampleIndex = secToSample(playTime, sampleLate)

    oldPos = ()
    nowPos = ()

    for i in range(int(lineLength / lineStep)):
        relativeSampleIndex = sampleIndex - i*lineStep
        percentage = 1 - i*lineStep / lineLength
        try:
            leftSample = audiData[relativeSampleIndex][0]
            rightSample = audiData[relativeSampleIndex][1]
        except:
            leftSample = 0
            rightSample = 0

        # 오른쪽 채널이 Y 축 이기에 따로 반전
        x, y = leftSample*osiloscopeRadius, rightSample*-osiloscopeRadius
        x += screenCenter[0]
        y += screenCenter[1]
        x = int(x)
        y = int(y)

        if i == 0:
            nowPos = (x, y)
        else:
            oldPos = nowPos
            nowPos = (x, y)

            # 이전점과 현재점간의 거리가 길수록 밀도가 낮아져 밝기도 낮아짐
            if distance(oldPos, nowPos) > 0:
                brightness = 1 / distance(oldPos, nowPos)**0.5
            else:
                brightness = 1
            
            if brightness > 1: brightness = 1

            # percentage 를 통해 선의 꼬리 끝으로 갈수록 어둡게 함
            brightness *= percentage
            # 밝기를 설정된 최소 밝기 이상으로 설정함
            brightness *= 1-minLineBrightness
            brightness += minLineBrightness
            
            if brightness < 0.5: # 밝기가 기준치 이하면
                # brightness 를 0 ~ 0.5 범위를 기준으로 정규화 해서 그만큼 색을 어둡개 함
                finalColor = (
                    int(lineColor[0] * brightness*2),
                    int(lineColor[1] * brightness*2),
                    int(lineColor[2] * brightness*2),
                    brightness * 255
                )
            else: # 밝기가 기준치 이상이면
                # brightness 를 0.5 ~ 1 범위를 기준으로 정규화 해서 그만큼 색을 밝게 함
                finalColor = (
                    int(lineColor[0] + (255-lineColor[0]) * (brightness*2-1)),
                    int(lineColor[1] + (255-lineColor[1]) * (brightness*2-1)),
                    int(lineColor[2] + (255-lineColor[2]) * (brightness*2-1)),
                    brightness * 255
                )

            pygame.draw.line(osiloscopeSurface, finalColor, oldPos, nowPos, 2)

    screen.blit(osiloscopeSurface, (0, 0))



    # 격자 그리기
    # 상하좌우 같은 기본적인 격자 모양
    gridShape = [
        # 중앙 십가자
        ( # 세로선
            (screenCenter[0], screenCenter[1]-osiloscopeRadius),
            (screenCenter[0], screenCenter[1]+osiloscopeRadius)
        ), ( # 가로선
            (screenCenter[0]-osiloscopeRadius, screenCenter[1]),
            (screenCenter[0]+osiloscopeRadius, screenCenter[1])
        ), 
        # 상하좌우 끝 마커
        ( # 상
            (screenCenter[0]-osiloscopeRadius/5, screenCenter[1]-osiloscopeRadius),
            (screenCenter[0]+osiloscopeRadius/5, screenCenter[1]-osiloscopeRadius)
        ), ( # 하
            (screenCenter[0]-osiloscopeRadius/5, screenCenter[1]+osiloscopeRadius),
            (screenCenter[0]+osiloscopeRadius/5, screenCenter[1]+osiloscopeRadius)
        ), ( # 우ㅜㅜㅜㅜㅜㅜㅜㅜㅜㅜㅜㅜㅜㅜ
            (screenCenter[0]-osiloscopeRadius, screenCenter[1]-osiloscopeRadius/5),
            (screenCenter[0]-osiloscopeRadius, screenCenter[1]+osiloscopeRadius/5)
        ), ( # 좌
            (screenCenter[0]+osiloscopeRadius, screenCenter[1]-osiloscopeRadius/5),
            (screenCenter[0]+osiloscopeRadius, screenCenter[1]+osiloscopeRadius/5)
        ), 
        # 상하좌우 중간 마커
        (
            (screenCenter[0]-osiloscopeRadius/10, screenCenter[1]-osiloscopeRadius/2),
            (screenCenter[0]+osiloscopeRadius/10, screenCenter[1]-osiloscopeRadius/2)
        ), (
            (screenCenter[0]-osiloscopeRadius/10, screenCenter[1]+osiloscopeRadius/2),
            (screenCenter[0]+osiloscopeRadius/10, screenCenter[1]+osiloscopeRadius/2)
        ), (
            (screenCenter[0]+osiloscopeRadius/2, screenCenter[1]-osiloscopeRadius/10),
            (screenCenter[0]+osiloscopeRadius/2, screenCenter[1]+osiloscopeRadius/10)
        ), (
            (screenCenter[0]-osiloscopeRadius/2, screenCenter[1]-osiloscopeRadius/10),
            (screenCenter[0]-osiloscopeRadius/2, screenCenter[1]+osiloscopeRadius/10)
        )
    ]

    for line in gridShape:
        pygame.draw.line(screen, (20, 20, 20), line[0], line[1], 2)

    # 0.1 마다 있는 세부 격자 그리기 
    # y축
    yMaker = screenCenter[1]-osiloscopeRadius
    for y in range(20):
        absY = yMaker + y* osiloscopeRadius/10
        pygame.draw.line(screen, (20, 20, 20),
            (screenCenter[0]-osiloscopeRadius/20, absY),
            (screenCenter[0]+osiloscopeRadius/20, absY), 2)

    # x 축
    xMaker = screenCenter[0]-osiloscopeRadius
    for x in range(20):
        absX = xMaker + x* osiloscopeRadius/10
        pygame.draw.line(screen, (20, 20, 20),
            (absX, screenCenter[1]-osiloscopeRadius/20),
            (absX, screenCenter[1]+osiloscopeRadius/20), 2)

    # 큰 원
    pygame.draw.circle(screen, (20, 20, 20), screenCenter, osiloscopeRadius, 2)
    # 작은 원
    pygame.draw.circle(screen, (20, 20, 20), screenCenter, osiloscopeRadius/2, 2)


    pygame.display.flip()
