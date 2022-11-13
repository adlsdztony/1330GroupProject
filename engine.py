import os
import time
import threading
import copy

from config import *
from monster_functions import *

clear = 'cls' if os.name == 'nt' else 'clear'

def getchar():
    ch = ''
    try:
        import msvcrt
        ch = msvcrt.getch()
    except:
        import tty, termios, sys
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

class Game:
    def __init__(self, init_map, fps=FPS):
        self.map_ = init_map
        self.in_game = True
        self.fps = fps
        self.t = None
        self.state = None
    
    def player_update(self, input_):
        if input_ in MOVE_DICT.keys():
            if self.map_.player_move(MOVE_DICT[input_]):
                self.in_game = False
                self.state = 'win'
    
    def main_thread(self):
        while self.in_game:
            state = self.map_.UpdateAndShow()
            if not state:
                self.state = 'dead'
                self.in_game = False
            time.sleep(1/self.fps)
            os.system(clear)
        if self.state is not None:
            self.map_.ShowMap()
            print(f'You {self.state}!')
            print('press any keys to contiune')
    
    def start_game(self):
        self.t = threading.Thread(target=self.main_thread)
        self.t.start()
        while self.in_game == True:
            a = chr(ord(getchar()))
            if a == 'E':
                self.in_game = False
                self.state = 'exit'
                break
            self.player_update(a)
        self.t.join()
        return self.state

class Map:
    def __init__(self, init_map, default_func=CatchOrRandom):
        self.player = None
        self.agent_list = []
        self.map_ = [list(i) for i in init_map]
        self.row = len(init_map)-2
        self.col = len(init_map[0])-2
        self.default_func = default_func
        for rn, row in enumerate(self.map_):
            for cn, col in enumerate(row):
                if col == 'P':
                    self.add_player([cn, rn])
                    self.map_[rn][cn] = ' '
                if col in MONSTERS.keys():
                    self.add_monster([cn, rn], func=MONSTERS[col],name=col if SHOW_TYPE_OF_MONSTER else 'M')
                    self.map_[rn][cn] = ' '
        self.count = 0

    def add_player(self, posi):
        if self.is_valid(posi): 
            self.player = agent('P', posi)
    
    def add_monster(self, posi, func=None, name='M'):
        if self.is_valid(posi):
            self.agent_list.append(agent(name, posi, self.default_func if func is None else func))
    
    def add_block(self, posi):
        if self.is_valid(posi):
            self.map_[posi[1]][posi[0]] = '#'
    
    def is_validp(self, posi):
        if posi[0] <= self.col+1 and posi[1] <= self.row+1:
            if self.map_[posi[1]][posi[0]] != '#':
                return True
            else:
                return False
    
    def is_valid(self, posi):
        if posi[0] <= self.col and posi[1] <= self.row and posi[0] > 0 and posi[1] > 0:
            if self.map_[posi[1]][posi[0]] != '#':
                return True
            else:
                return False
    
    def player_move(self, direction, ag=None):
        if ag is None:
            ag = self.player
        new_posi = [ag.posi[0]+direction[0], ag.posi[1]+direction[1]]
        if self.is_validp(new_posi):
            ag.posi = new_posi
        if ag.posi[1] > self.row or ag.posi[0] > self.col or ag.posi[0] == 0 or ag.posi[1] == 0:
            return True
        return False
        
    def map_now(self):
        temp_map = copy.deepcopy(self.map_)
        temp_map[self.player.posi[1]][self.player.posi[0]] = 'P'
        for ag in self.agent_list:
            temp_map[ag.posi[1]][ag.posi[0]] = ag.name
        return temp_map
    
    def get_around(self, ag):
        map_now = self.map_now()
        posi = ag.posi
        around = [[map_now[posi[1]+i][posi[0]+j] for j in range(-1, 2)] for i in range(-1, 2)]
        return around
    
    def ag_move(self):
        for ag in self.agent_list:
            new_posi = ag.move(self.get_around(ag), self.count)
            if self.is_valid(new_posi):
                ag.posi = new_posi
    
    def ShowMap(self):
        for row in self.map_now():
            print(' '.join(row))

    def UpdateAndShow(self):
        self.count += 1
        self.ag_move()
        for ag in self.agent_list:
            if ag.posi == self.player.posi:
                return False
        self.ShowMap()
        return True

class agent:
    def __init__(self, name, init_posi, mov_func=CatchOrRandom):
        self.posi = init_posi
        self.name = name
        self.mov_func = mov_func
    
    def move(self, around, state):
        m = self.mov_func(around, state)
        return [self.posi[i] + m[i] for i in [0, 1]]


if __name__ == '__main__':
    map_ = [
        '#### ##',
        '#P    #',
        '#     #',
        '#     #',
        '#     #',
        '    M  ',
        '# #####',
        '#     #'
        ]
    b = Map(map_)

    game = Game(b)
    game.start_game()
