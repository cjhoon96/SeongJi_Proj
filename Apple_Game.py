import pygame as pg
import random, os

from pathlib import Path

# 파이썬 실행 경로 수정
DIR = Path(__file__).parent.absolute()
DIR = f'{DIR}'.replace('\\','/')
os.chdir(DIR)

image_path = './img/' # 이미지 파일 경로
bckgrd_color =(10,10,10) # 배경 색, 검은색


class Apple(pg.sprite.Sprite):
    # 사과 클래스, Sprite 클래스로 만들었음.

    def __init__(self, number, pos):
        self.number = number
        self.pos = pos

        # Sprite 클래스가 기본적으로 가지고 있는 것들
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([60,60])
        self.image = pg.image.load(image_path + f'img{number}.png')
        self.rect = self.image.get_rect()

    def destroy(self):
        self.number = 10
        self.image.fill(bckgrd_color)


def init_apples():
    # 게임 시작 시 실행할 함수, 사과 배열을 만듬
    board = [[random.randint(1, 9) for _ in range(10)] for _ in range(10)]  # 일단은 10 x 10 배열로 만듦. 나중에 이미지 크기와 함께 조정해야함.
    apples = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            apples.append(Apple(board[i][j], (60*i,60*j)))  # 지금 이미지가 60픽셀짜리라서 간격도 60

    return apples

def draw_apples(apples):
    # apples : 사과 배열
    # 사과 배열을 받아서 화면에 그려주는 함수
    screen.fill(bckgrd_color)
    for apple in apples:
        screen.blit(apple.image, (apple.pos[0], apple.pos[1]))
        
        

pg.init()

# Screen
screen_width, screen_height = 600, 600
size = [screen_width, screen_height]
screen = pg.display.set_mode(size)
screen.fill(bckgrd_color)

# 드래그 직사각형 그리기 위한 변수
drawing = False
dSize = (0,0)
start = (0,0)
end = (0,0)

apples = init_apples()

playing = True
# Game loop
while playing:
    events = pg.event.get()
    
    for event in events:
        if event.type == pg.QUIT:
            playing = False

        elif event.type == pg.MOUSEBUTTONDOWN:
            drawing = True
            start = event.pos
            
        elif event.type == pg.MOUSEBUTTONUP:
            end = event.pos
            drawing = False
            draw_apples(apples)

        elif event.type == pg.MOUSEMOTION and drawing:
            end = event.pos
            dSize = end[0]-start[0], end[1]-start[1]
            rect = pg.Rect(start, dSize)
            draw_apples(apples)
            pg.draw.rect(screen, pg.Color(10,150,10), rect, 4)

    
    pg.display.flip()