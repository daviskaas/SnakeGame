
import pygame as pg
import sys
import constants as const
import objects as obj
from pathlib import Path
import random

pg.init()
pg.font.init()

pg.display.set_caption('Snake Game')
display = pg.display.set_mode((const.WIDTH,const.HEIGHT))

assets = Path('assets')

grass_surface = pg.Surface((const.SIZE[0] * const.N_CELS[0],const.SIZE[1] * const.N_CELS[1]))
grass_img = pg.image.load(assets / 'grass.png')
for i in range(const.MAX_CELS):
    grass_img = pg.transform.rotate(grass_img,90*random.randrange(3))
    coord = divmod(i,const.N_CELS[1])
    pos = [coord[0] * const.SIZE[0] , coord[1] * const.SIZE[1]]
    grass_surface.blit(grass_img,pos)


def draw_game():
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            sys.exit()
    
        if ev.type == pg.KEYUP:
            if not const.PAUSED:
                snake.handle_event(ev)
            if ev.key == pg.K_p:
                const.PAUSED = not const.PAUSED

    
            
    display.blit(grass_surface,(0,0))
            
    snake.draw(display)
    snack.draw(display)
    
    if not const.PAUSED:
        snake.update(.5)
        snack.update()
    else:
        p = pg.Surface((const.WIDTH,const.HEIGHT)) ; p.set_alpha(255 * 0.4)
        display.blit(p,(0,0))


font = pg.font.SysFont('calibri',50)
def draw_finish_screen():
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            sys.exit()

        if ev.type == pg.KEYUP:
            if ev.key == pg.K_r:
                snake.reset()

    stats_text = f"You {['Lost','Win'][int(snake.win)]}!"
    f = font.render(stats_text,True,'black')
    display.blit(f,((const.WIDTH - f.get_width())//2,0))

    reset_text = 'Press R to reset'
    f = font.render(reset_text,True,'black')
    display.blit(f,((const.WIDTH - f.get_width())//2,50))

RUNNING = True
snake = obj.Snake()
snack = obj.Snack(snake)

while RUNNING:
    display.fill([90]*3)
    clock = pg.time.Clock()

    if snake.alive:
        draw_game()

    else:
        draw_finish_screen()

    clock.tick(60)
    pg.display.update()

