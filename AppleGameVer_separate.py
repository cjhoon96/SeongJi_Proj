import pygame as pg
import random, os
import time
import sys

from pathlib import Path
 
pg.init()                                                   #성재 이거 여기로 옮겨써
pg.mixer.init()                                             #mixer 초기화

# 파이썬 실행 경로 수정
DIR = Path(__file__).parent.absolute()
DIR = f'{DIR}'.replace('\\','/')
os.chdir(DIR)

# 드래그 직사각형 그리기 위한 변수
drawing = False
dSize = (0,0)
start = (0,0)
end = (0,0)
playing = True
timeover = False
waiting = True

class Apple(pg.sprite.Sprite):
    # 사과 클래스, Sprite 클래스로 만들었음.

    def __init__(self, number, pos):
        self.number = number # 사과에 쓰여있는 숫자
        self.pos = pos       # 사과 위치

        # Sprite 클래스가 기본적으로 가지고 있는 것들
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(f'./img/img{number}.png')
        self.rect = self.image.get_rect(center = (pos[0]+15, pos[1]+15))

    def destroy(self):
        # 사과 없애는 함수
        global score                                    #score global 선언
        self.number = 0
        apples.remove(self)
        score += 1                                      #스코어 1 추가


def init_apples():
    # 게임 시작 시 실행할 함수, 사과 배열을 만듬
    board = [[random.randint(0, 9) for _ in range(20)] for _ in range(20)]
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
        
def is_ten(rect):
    # 드래그해서 만든 rect와 만나는 사과들의 사과수를 더해서 10이면 사과를 지우는 함수
    # rect: 드래그해서 만든 직사각형
    inside_apples = pg.Rect.collidelistall(rect, [apple.rect for apple in apples]) # collidelistall : rect와 부딪힌 list안의 rect들의 index를 모두 리턴하는 함수
    total_sum = sum([apples[idx].number for idx in inside_apples])
    if total_sum == 10:
        for idx in inside_apples[::-1]:
            apples[idx].destroy()
        pop.set_volume(vol)
        pg.mixer.Sound.play(pop)
    return total_sum

def draw_time():
    # 타이머 그리는 함수
    global timeover, start_ticks # 타이머가 0이 되면 timeover를 True로 바꿈

    # 타이머 그 밖에 하얀 네모
    timer_case_pos = (10, 45)
    timer_case_size = (630, 20)
    timer_case_rect = pg.Rect(timer_case_pos,timer_case_size)

    # 시간 계산
    curr_time = pg.time.get_ticks() - start_ticks
    timer_len = timer_case_size[0] -10 - (curr_time*timer_case_size[0])/60000
    timer_polygon = ((15, 50), (15, 59), (15+timer_len, 59), (15+timer_len, 50))

    pg.draw.rect(ui_surf, pg.Color(250,250,250), timer_case_rect, 3)
    pg.draw.polygon(ui_surf, pg.Color(50,150,50), timer_polygon)

    if timer_len < 0:
        timeover = True

def blit_ui(score):
    # UI 출력 함수
    ui_surf.fill(pg.Color(110,110,110))

    n_score = game_font.render("Score: " + str(int(score)), True, (200,200,200))  # 점수 글자
    font_pos = (10, 10)                          # 글자 위치
    mute_pos = (660, 10)                         # 볼륨 위치

    ui_surf.blit(n_score, font_pos)              # 점수 출력
    ui_surf.blit(mute[vol_idx], mute_pos)        # 볼륨 크기 출력
    draw_time()                                  # 타이머 출력

    screen.blit(ui_surf, (0,725))                # ui_surf를 전체 화면에 blit


game_font = pg.font.SysFont(None, 30)                        #폰트 설정
pop = pg.mixer.Sound("./sound/pop.wav")                     #효과음 변수 지정
vol_idx = 1                                    # vol_idx 현재 볼륨이 0인지 1인지 2인지 3인지
vol = 0.3                                      #음소거,해제 관련 변수 디폴트 = 음소거 해제
press_check = True                                          #중복 방지

bckgrd_color =(10,10,10) # 배경 색, 검은색
UI_padding = (20, 20)    # 전체 창과의 간격
apple_padding = 5        # 사과끼리 간격

score = 0                                      #score 초기화
timeover = False

# icons
mute_size = (50,50)
mute = []
mute.append(pg.image.load('./img/touch_0.png'))
mute.append(pg.image.load('./img/touch_1.png'))
mute.append(pg.image.load('./img/touch_2.png'))
mute.append(pg.image.load('./img/touch_3.png'))
mute = [pg.transform.scale(image,mute_size) for image in mute]                           #싱기방기

apple_icons = []
apple_icons.append(pg.image.load('./img/touch_0.png'))                    #아이콘 구하면 수정
apple_icons.append(pg.image.load('./img/touch_1.png'))
apple_icons = [pg.transform.scale(image,(10,10)) for image in apple_icons]
button = apple_icons[0]
button_on = apple_icons[1]

# Screen
screen_width, screen_height = 735, 800                     #아래 여백 만들기
screen_size = [screen_width, screen_height]
screen = pg.display.set_mode(screen_size)
screen.fill(bckgrd_color)

# UI Surface: 타이머, 스코어, 볼륨 아이콘들을 출력할 Surface
ui_surf = pg.Surface((screen_width, 75))

# Start page, 게임 시작 시 화면
start_screen = pg.Surface(screen_size)



# 사과들 초기화
apples = init_apples()

# 타이머
clock = pg.time.Clock()




class Button:
    def __init__(self, img_in, x, y, width, height, img_act, x_act, y_act, action):
        self.img_in = img_in
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img_act = img_act
        self.x_act = x_act
        self.y_act = y_act
        self.action = action
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            start_screen.blit(img_act, (x_act, y_act))
            if click[0] and action != None:
                time.sleep(1)
                action
            else:
                start_screen.blit(img_in,(x,y))

def quitgame():
    pg.quit()
    sys.exit()

def start_menu():
    menu = True
    
    while menu:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quitgame()
        
        start_screen.fill(pg.Color(50,100,50))
        title_font = game_font.render("APPLE GAME", True, (200,200,200))
        start_font = game_font.render("Start ", True, (200,200,200))  # 점수 글자
        start_screen.blit(title_font, (300, 200))
        start_screen.blit(start_font, (300, 350))
        screen.blit(start_screen, (0,0))
        startButton = Button(button, 250, 220, 100, 100, button_on, 250, 220, playing())
        pg.display.flip()
        clock.tick(15)

def playing():
    global playing , timeover, waiting, start, end, dSize, start_ticks
    # Game loopdrawing = False
    while playing:
        clock.tick(60)
        # 처음 게임 시작시 클릭할 때까지 대기
        if waiting:                             
            while True:
                start_screen.fill(pg.Color(0,0,0))
                pg.display.flip()
                event = pg.event.wait()
                if event.type == pg.QUIT:        # Quit
                    quitgame()

                elif event.type == pg.MOUSEBUTTONDOWN:  # 클릭하면 시작
                    waiting = False
                    start_ticks = pg.time.get_ticks()   # 타이머 시작
                    break

        events = pg.event.get()
        rect = pg.Rect(start, dSize)
        for event in events:
            if event.type == pg.QUIT:
                quitgame()

            elif event.type == pg.MOUSEBUTTONDOWN:
                drawing = True
                start = event.pos

            elif event.type == pg.MOUSEBUTTONUP:
                end = event.pos
                drawing = False
                is_ten(rect)
                draw_apples(apples)
                blit_ui(score)
                
            elif event.type == pg.MOUSEMOTION and drawing:
                end = event.pos
                dSize = end[0]-start[0], end[1]-start[1]
                rect = pg.Rect(start, dSize)
                draw_apples(apples)
                pg.draw.rect(screen, pg.Color(10,150,10), rect, 2)

            elif event.type == pg.KEYDOWN:  #mute 기능 upgrade
                if event.key == pg.K_m:
                    # Mute            
                    if press_check:
                        if vol_idx:
                            vol_idx = 0
                            vol = 0
                        elif not vol_idx:
                            vol_idx = 3
                            vol = 0.9
                            pop.set_volume(vol)
                            pg.mixer.Sound.play(pop) 

                elif event.key == pg.K_UP:
                    # Volume Up
                    if press_check and vol_idx < 3:
                        vol_idx += 1
                        vol += 0.3
                        pop.set_volume(vol)
                        pg.mixer.Sound.play(pop)

                elif event.key == pg.K_DOWN:
                    # Volume Down
                    if press_check and vol_idx > 0:
                        vol_idx -= 1
                        vol -= 0.3
                        pop.set_volume(vol)
                        pg.mixer.Sound.play(pop)
                
                press_check = False

            elif event.type == pg.KEYUP:
                if not press_check:
                    press_check = True
                    
        blit_ui(score)

        pg.display.flip()

        if timeover:                             # Time over 시 게임 멈춤
            while True:
                event = pg.event.wait()
                if event.type == pg.QUIT:        # Quit
                    playing = False
                    break
