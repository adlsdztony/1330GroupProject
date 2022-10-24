import os
import time
import threading
import copy
from random import randint
from tkinter import W

from config import *

class Game:
    def __init__(self, init_map, fps=FPS):
        self.map_ = init_map
        self.in_game = True
        self.fps = fps
        self.t = None
        self.dead = False
    
    def update(self, input_):
        if input_ == 'w':
            self.map_.player_move([0, -1])
        elif input_ == 'a':
            self.map_.player_move([-1, 0])
        elif input_ == 's':
            self.map_.player_move([0, 1])
        elif input_ == 'd':
            self.map_.player_move([1, 0])
    
    def main_thread(self):
        while self.in_game:
            state = self.map_.show()
            if not state:
                self.dead = True
                self.in_game = False
            time.sleep(1/self.fps)
            os.system('cls' if os.name == 'nt' else 'clear')
        if self.dead:
            print('You dead!')
        print('Bye!')
    
    def start_game(self):
        self.t = threading.Thread(target=self.main_thread)
        self.t.start()
        while self.in_game == True:
            a = input()
            if a == 'E':
                self.in_game = False
                break
            self.update(a)

class Map:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.map_ = [['#' for i in range(col+2)]]
        for r in range(row):
            self.map_.append(list('#'+' '*col+'#'))
        self.map_.append(['#' for i in range(col+2)])
        self.player = None
        self.agent_list = []
        self.count = 0

    def add_player(self, posi):
        if self.is_valid(posi): 
            self.player = agent('P', posi)
    
    def add_monster(self, posi):
        if self.is_valid(posi):
            self.agent_list.append(agent('M', posi))
    
    def add_block(self, posi):
        if self.is_valid(posi):
            self.map_[posi[1]][posi[0]] = '#'
    
    def is_valid(self, posi):
        if posi[0] <= self.col and posi[1] <= self.row:
            if self.map_[posi[1]][posi[0]] != '#':
                return True
            else:
                return False
    
    def player_move(self, direction, ag=None):
        if ag is None:
            ag = self.player
        new_posi = [ag.posi[0]+direction[0], ag.posi[1]+direction[1]]
        if self.is_valid(new_posi):
            ag.posi = new_posi
        
    
    def map_now(self):
        temp_map = copy.deepcopy(self.map_)
        temp_map[self.player.posi[1]][self.player.posi[0]] = 'P'
        for ag in self.agent_list:
            temp_map[ag.posi[1]][ag.posi[0]] = ag.name
        return temp_map
    
    def ag_move(self):
        for ag in self.agent_list:
            new_posi = ag.random_move()
            if self.is_valid(new_posi):
                ag.posi = new_posi

    def show(self):
        self.count += 1
        if self.count % FPS == 0:
            self.ag_move()
        for ag in self.agent_list:
            if ag.name == 'M':
                if ag.posi == self.player.posi:
                    return False
        for row in self.map_now():
            print(' '.join(row))
        return True

class agent:
    def __init__(self, name, init_posi):
        self.posi = init_posi
        self.name = name
    
    def random_move(self):
        return [self.posi[0]+randint(-1, 1), self.posi[1]+randint(-1, 1)]

if __name__ == '__main__':
    b = Map(5, 5)
    b.add_player([2, 2])
    b.add_monster([2, 3])
    b.add_monster([3, 3])
    b.add_block([3, 4])

    game = Game(b)
    game.start_game()
