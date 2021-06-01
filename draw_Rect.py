import pygame as pg

pg.init()

# Screen
screen_width, screen_height = 630, 630
size = [screen_width, screen_height]
screen = pg.display.set_mode(size)
bckgrd_color =(20,20,20)
screen.fill(bckgrd_color)

drawing = False
dSize = (0,0)
start = (0,0)
end = (0,0)

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
            screen.fill(bckgrd_color)

        elif event.type == pg.MOUSEMOTION and drawing:
            end = event.pos
            dSize = end[0]-start[0], end[1]-start[1]
            rect = pg.Rect(start, dSize)
            screen.fill(bckgrd_color)
            pg.draw.rect(screen, pg.Color(100,100,100),rect, 2)
            
    pg.display.flip()