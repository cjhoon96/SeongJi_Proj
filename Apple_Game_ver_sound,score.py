import pygame as pg
import random, os
import time

from pathlib import Path
 
pg.init()                                                   #성재 이거 여기로 옮겨써
pg.mixer.init()                                             #mixer 초기화

# 파이썬 실행 경로 수정
DIR = Path(__file__).parent.absolute()
DIR = f'{DIR}'.replace('\\','/')
os.chdir(DIR)

game_font = pg.font.SysFont(None,30)                        #폰트 설정
pop = pg.mixer.Sound("./sound/pop.wav")                     #효과음 변수 지정
sound_check = True                                          #음소거,해제 관련 변수 디폴트 = 음소거 해제
press_check = True                                          #중복 방지

image_path = './img/' # 이미지 파일 경로
bckgrd_color =(10,10,10) # 배경 색, 검은색
UI_padding = (20, 20)    # 전체 창과의 간격
apple_padding = 5        # 사과끼리 간격

score = 0                                               #score 초기화

class Apple(pg.sprite.Sprite):
    # 사과 클래스, Sprite 클래스로 만들었음.

    def __init__(self, number, pos):
        self.number = number # 사과에 쓰여있는 숫자
        self.pos = pos       # 사과 위치

        # Sprite 클래스가 기본적으로 가지고 있는 것들
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([30,30])
        self.image = pg.image.load(image_path + f'img{number}.png')
        self.rect = self.image.get_rect(center = (pos[0]+15, pos[1]+15))

    def destroy(self):
        # 사과 없애는 함수
        global score                                    #score global 선언
        self.number = 0
        self.image.fill(bckgrd_color)
        score += 1                                      #스코어 1 추가


def init_apples():
    # 게임 시작 시 실행할 함수, 사과 배열을 만듬
    board = [[random.randint(0, 9) for _ in range(20)] for _ in range(20)]  # 일단은 10 x 10 배열로 만듦. 나중에 이미지 크기와 함께 조정해야함.
    apples = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            apples.append(Apple(board[i][j], (30*i+UI_padding[0]+apple_padding*i,30*j+UI_padding[1]+apple_padding*j)))

    return apples

def draw_apples(apples):
    # apples : 사과 배열
    # 사과 배열을 받아서 화면에 그려주는 함수
    screen.fill(bckgrd_color)
    for apple in apples:
        screen.blit(apple.image, (apple.pos[0], apple.pos[1]))
    print('Draw apple')
        
def is_ten(rect):
    # 드래그해서 만든 rect와 만나는 사과들의 사과수를 더해서 10이면 사과를 지우는 함수
    # rect: 드래그해서 만든 직사각형
    inside_apples = pg.Rect.collidelistall(rect, [apple.rect for apple in apples]) # collidelistall : rect와 부딪힌 list안의 rect들의 index를 모두 리턴하는 함수
    total_sum = sum([apples[idx].number for idx in inside_apples])
    if total_sum == 10:
        for idx in inside_apples:
            apples[idx].destroy()
        if sound_check:
            pg.mixer.Sound.play(pop)                           #더해서 10이될시 pop 사운드를 출력
    return total_sum

def blit_score(score):
    # 점수 출력 함수
    n_score = game_font.render("Score: " + str(int(score)), True, (200,200,200))  # 점수 글자
    font_pos = (10, 725) # 글자 위치
    screen.blit(n_score, font_pos)


# Screen
screen_width, screen_height = 735, 815                     #아래 여백 만들기
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
    rect = pg.Rect(start, dSize)

    for event in events:
        if event.type == pg.QUIT:
            playing = False

        elif event.type == pg.MOUSEBUTTONDOWN:
            drawing = True
            start = event.pos

        elif event.type == pg.MOUSEBUTTONUP:
            end = event.pos
            drawing = False
            print(is_ten(rect))
            draw_apples(apples)
            blit_score(score)

        elif event.type == pg.MOUSEMOTION and drawing:
            end = event.pos
            dSize = end[0]-start[0], end[1]-start[1]
            rect = pg.Rect(start, dSize)
            draw_apples(apples)
            blit_score(score)
            pg.draw.rect(screen, pg.Color(10,150,10), rect, 2)

        elif event.type == pg.KEYDOWN and event.key == pg.K_m:             #mute 기능 추가
            if press_check:
                if sound_check:
                    sound_check = False
                elif not sound_check:
                    sound_check = True
                    pg.mixer.Sound.play(pop) 
                press_check = False

        elif event.type == pg.KEYUP and event.key == pg.K_m:
            if not press_check:
                press_check = True

    pg.display.flip()
