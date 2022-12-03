import constants as const
import pygame as pg
import random
import itertools
from pathlib import Path

posses = [(1,0),(0,0)]
dirn = (1,0)
assets = Path('assets')
class Snake(object):

    body = []
    turns = {}
    dirn = dirn
    tick_count = 0
    alive = True
    win = False

    def __init__(self):
        for pos in posses:
            self.body.append(SnakeCube(pos,dirn))

        self.head = self.body[0]

    def __len__(self):
        return len(self.body)
        
        
        
    def draw(self,surface):
        for i,cube in enumerate(self.body):
            cube.draw(surface)

    def reset(self):
        self.body = [SnakeCube(pos,dirn) for pos in posses]
        self.body.append(self.head)
        self.turns = {}
        self.dirn = dirn

        self.win = False
        self.alive = True

    def update(self,move_seg):
        self.tick_count += 1
        if self.tick_count% (const.FPS*move_seg) == 0:
            self.move()
            
            self.alive = self.__check_alive_status()
            self.win = self.__check_win_status()
            
    def __check_alive_status(self):
        cube_posses = [cube.pos for cube in self.body]

        auto_touched = len(cube_posses) != len(set(cube_posses))
        lean_barrer = False in [(x>-1 and x<const.N_CELS[0] and y>-1 and y<const.N_CELS[1]) for (x,y) in cube_posses]

        return not auto_touched and not lean_barrer

    def __check_win_status(self):
        return len(self) >= const.MAX_CELS

    def move(self):
        
        for i, cube in enumerate(self.body):
            p = cube.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                cube.dirn = turn
                if i == len(self)-1:
                    self.turns.pop(p)
            cube.move()

    def handle_event(self,ev):
        MOVE_KEYS = [pg.K_UP,pg.K_LEFT,pg.K_DOWN,pg.K_RIGHT]
        dirns  = [(0,-1),(-1,0),(0,1),(1,0)]
        
        key = ev.key
        if key in MOVE_KEYS:
            i = MOVE_KEYS.index(key)
            to_move_dirn = dirns[i]
            rdirn = tuple([_*-1 for _ in to_move_dirn])
            
            if rdirn != self.dirn:
            
                self.dirn = to_move_dirn
                self.turns[self.head.pos] = self.dirn

    def add_cube(self):
        tail = self.body[-1]
        rdirn = tuple([_*-1 for _ in tail.dirn])
        pos = (tail.pos[0] + rdirn[0],tail.pos[1] + rdirn[1])
        self.body.append(SnakeCube(pos,tail.dirn))
        
class SnakeCube(Snake):
    def __repr__(self) -> str:
        return f'SnakeCube({self.pos})'

    def __init__(self,pos,dirn) -> None:
        self.pos = pos
        self.dirn = dirn

    def draw(self,surface):
        x = self.pos[0] * const.SIZE[0]
        y = self.pos[1] * const.SIZE[1]

        pg.draw.rect(surface,'red',[x,y,*const.SIZE])
        pg.draw.rect(surface,'black',[x,y,*const.SIZE],1)
        
        
        
        #pg.draw.rect(surface,['black','red'][head],pos)

    def move(self):
        self.pos = (self.pos[0] + self.dirn[0], self.pos[1] + self.dirn[1])
    
        
class Snack(object):
    def __init__(self,snake) -> None:
        self.__snake = snake
        
        self.pos = self.gen_pos()

    def draw(self,surface):
        if self.pos != None:
            x = self.pos[0] * const.SIZE[0]
            y = self.pos[1] * const.SIZE[1]
            pos  = [x,y]
            img = pg.image.load(assets / 'snack.png')
            surface.blit(img,pos)
    def gen_pos(self):
        avaiable_spawn = itertools.product(*[range(_) for _ in const.N_CELS])
        avaiable_spawn = list(filter(lambda _:_ not in [cube.pos for cube in self.__snake.body] ,avaiable_spawn))
        if len(avaiable_spawn) != 0:
            return random.choice(avaiable_spawn)

    def update(self):
        if self.__snake.head.pos == self.pos:
            self.pos = self.gen_pos()
            self.__snake.add_cube()

    