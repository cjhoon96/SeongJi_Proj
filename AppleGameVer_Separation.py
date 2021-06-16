import pygame as pg
import random, os
import time
import sys

from pathlib import Path

from pygame.constants import MOUSEBUTTONDOWN
 
pg.init()                                                   #성재 이거 여기로 옮겨써
pg.mixer.init()                                             #mixer 초기화

# 파이썬 실행 경로 수정
DIR = Path(__file__).parent.absolute()
DIR = f'{DIR}'.replace('\\','/')
os.chdir(DIR)

# icons
mute_size = (50,50)
mute = []
mute.append(pg.image.load('./img/touch_0.png'))
mute.append(pg.image.load('./img/touch_1.png'))
mute.append(pg.image.load('./img/touch_2.png'))
mute.append(pg.image.load('./img/touch_3.png'))
mute = [pg.transform.scale(image,mute_size) for image in mute]                           #싱기방기

apple_icons = []
apple_icons.append(pg.image.load('./img/apple-icon.png'))                    #아이콘 구하면 수정
apple_icons.append(pg.image.load('./img/apple-half-icon.png'))

#font, sound
game_font = pg.font.SysFont(None, 30)                        #폰트 설정
pop = pg.mixer.Sound("./sound/pop.wav")                     #효과음 변수 지정
vol_idx = 1                                    # vol_idx 현재 볼륨이 0인지 1인지 2인지 3인지
vol = 0.3                                      #음소거,해제 관련 변수 디폴트 = 음소거 해제


# Screens
screen_width, screen_height = 735, 800                      #아래 여백 만들기
screen_size = [screen_width, screen_height]
screen = pg.display.set_mode(screen_size)                   #게임 플레이 스크린
start_screen = pg.display.set_mode(screen_size)             #시작메뉴 스크린

# UI Surface: 타이머, 스코어, 볼륨 아이콘들을 출력할 Surface
ui_surf = pg.Surface((screen_width, 75))



bckgrd_color =(10,10,10) # 배경 색, 검은색
UI_padding = (20, 20)    # 전체 창과의 간격
apple_padding = 5        # 사과끼리 간격


# Game loopdrawing = False

# 타이머
clock = pg.time.Clock()
screen.fill(bckgrd_color)
# 드래그 직사각형 그리기 위한 변수
drawing = False
dSize = (0,0)
start = (0,0)
end = (0,0)
playing = True
timeover = False
waiting = True
press_check = True                                          #중복 방지
score = 0                                      #score 초기화
timeover = False
pop_score = 0
easy = False
plus_time = 0

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
        global score,  pop_score                          #score global 선언
        self.number = 0
        apples.remove(self)
        score += 1                                      #스코어 1 추가
        pop_score += 1

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
    global timeover, start_ticks, pop_score, plus_time # 타이머가 0이 되면 timeover를 True로 바꿈
    start_ticks = int(start_ticks)
    # 타이머 그 밖에 하얀 네모
    timer_case_pos = (10, 45)
    timer_case_size = (630, 20)
    timer_case_rect = pg.Rect(timer_case_pos,timer_case_size)
    

    if easy and pop_score >= 3:
        start_ticks += 3000
        pop_score = 0

    # 시간 계산
    curr_time = pg.time.get_ticks() - start_ticks
    timer_len = timer_case_size[0] -10 - (curr_time*timer_case_size[0])/60000
    if timer_len > 620:
        timer_len = 620
    timer_polygon = ((15, 50), (15, 59), (15+timer_len, 59), (15+timer_len, 50))
    if timer_len >= 0:
        pg.draw.rect(ui_surf, pg.Color(250,250,250), timer_case_rect, 3)
    if timer_len > 0:
        pg.draw.polygon(ui_surf, pg.Color(50,150,50), timer_polygon)
    else:
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


def Button(screen, icon1, icon2, x, y, boolean):
    if boolean:
        screen.blit(icon2,(x,y))
    else:
        screen.blit(icon1,(x,y))
def check_on(l_x, t_y, r_x, b_y):
    mouse = pg.mouse.get_pos()
    if l_x <= mouse[0] <= r_x and t_y <= mouse[1] <= b_y:
        return True
    else:
        return False



#게임 종료 함수
def quitgame():
    pg.quit()
    sys.exit()


#시작 메뉴 함수
def start_menu():
    global apple_icons, easy, timeover, score
    apple_icons = [pg.transform.scale(image,(35,35)) for image in apple_icons]
    menu = True
    startButton = False
    title_font = pg.font.SysFont(None, 70) 
    start_font = pg.font.SysFont(None, 60)
    diff_font = pg.font.SysFont(None, 25)
    title = title_font.render("APPLE GAME", True, (200,200,200))
    start_button = start_font.render("Start ", True, (200,200,200))  # 점수 글자
    ez_button_1 = diff_font.render("EZ!!!!!!!!!", True, (200,200,200))
    ez_button_2 = diff_font.render("EZ!!!!!!!!!", True, (255,255,0))
    nor_button_1 = diff_font.render("NORMAL", True, (200,200,200))
    nor_button_2 = diff_font.render("NORMAL", True, (255,255,0))
    diffButton = False
    startpress = False
    diffpress = False
    while menu:
        for event in pg.event.get():
            startButton = check_on(30, 570, 150, 610)
            diffButton = check_on(30, 630, 150, 650)
            if event.type == pg.QUIT:
                quitgame()     
            start_screen.fill(pg.Color(50,100,50))
            start_screen.blit(title, (30, 500))
            start_screen.blit(start_button, (30, 570))
            
            Button(start_screen, apple_icons[0], apple_icons[1], 130, 570, startButton)
            
            if startButton and event.type == pg.MOUSEBUTTONDOWN:
                startpress = True
            elif startpress and event.type == pg.MOUSEBUTTONUP:
                if startButton:
                    timeover = False
                    score = 0
                    return play()
                else:
                    startpress = False
            
            if diffButton and event.type == pg.MOUSEBUTTONDOWN:
                diffpress = True
            if diffpress and event.type == pg.MOUSEBUTTONUP:
                if diffButton:
                    if easy:
                        easy = False
                    else:
                        easy = True
                else:
                    diffpress = False
            
            if easy:
                if diffButton:
                    start_screen.blit(ez_button_2, (30, 630))
                else:
                    start_screen.blit(ez_button_1, (30, 630))
            else:
                if diffButton:
                    start_screen.blit(nor_button_2, (30, 630))
                else:
                    start_screen.blit(nor_button_1, (30, 630))

        pg.display.flip()

#게임 실행 함수
def play():
    global playing , timeover, waiting, start, end, dSize, start_ticks, drawing, apples, press_check, pop_score, vol_idx, vol
    # 사과들 초기화
    apples = init_apples()
    start_ticks = pg.time.get_ticks()   # 타이머 시작
    draw_apples(apples)
    while playing:
        pop_score = 0
        clock.tick(60)

        if timeover:                             # Time over 시 게임 멈춤
            break     

        events = pg.event.get()
        rect = pg.Rect(start, dSize)
        for event in events:
            draw_apples(apples)
            blit_ui(score)
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

    last_menu(score)                                                        ## 이부분에서 오류

def print_apple(n,x,y,size,screen):
    global apple_icons
    apple_icons = [pg.transform.scale(image,(size,size)) for image in apple_icons]
    lines = n // 20
    last_line = n % 20
    if lines:
        for i in range(lines):
            for j in range(20):
                screen.blit(apple_icons[1],(x + (j * size),y + (i * size)))
        y += (lines * size)
    for i in range(20):
        if i < last_line:
            screen.blit(apple_icons[1],(x + (i * size), y))
        else:
            screen.blit(apple_icons[0],(x + (i * size), y))
    y += size
    for i in range(20 - 1 -lines):
        for j in range(20):
            screen.blit(apple_icons[0],(x + (j * size),y + (i * size)))

#게임 결과 함수    
def last_menu(scr):
    global timeover, score
    score_font = pg.font.SysFont(None, 60)
    
    i = 0
    last = True
    againpress = False
    menupress = False
    while last:
        events = pg.event.get()
        
        for event in events:
            againButton = check_on(296, 500, 440, 540)
            menuButton = check_on(302, 600, 430, 640)
            if event.type == pg.QUIT:
                quitgame()
            result_screen = pg.display.set_mode(screen_size)
            result_screen.fill(bckgrd_color)
            score_p = score_font.render("SCORE: " + str(int(i)), True, (200,200,200))  # 점수 글자
            result_screen.blit(score_p, (255, 100))
            print_apple(i,210,150,15,result_screen)
            if i < scr:
                i += 1
                pg.display.flip() 
                time.sleep(0.2)
                continue
            if againButton:
                again = score_font.render("AGAIN",True,(255,255,0))
            else:
                again = score_font.render("AGAIN",True,(200,200,200))
            if menuButton:
                menu = score_font.render("MENU",True,(255,255,0))
                
            else:
                menu = score_font.render("MENU",True,(200,200,200))
            if againButton and event.type == pg.MOUSEBUTTONDOWN:
                againpress = True
            elif againpress and event.type == pg.MOUSEBUTTONUP:
                if againButton:
                    timeover = False
                    score = 0
                    return play()
                else:
                    againpress = False
            elif menuButton and event.type == pg.MOUSEBUTTONDOWN:
                menupress = True
            elif menupress and event.type == pg.MOUSEBUTTONUP:
                if menuButton:
                    return start_menu()
                else:
                    menupress = False
                
            result_screen.blit(again,(296,500))
            result_screen.blit(menu,(302,600))
            
        pg.display.flip() 
        n = 0


start_menu()