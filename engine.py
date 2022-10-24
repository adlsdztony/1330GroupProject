import os
import time
import threading
import copy

from config import *

class Game:
    def __init__(self, init_map, fps=FPS):
        self.map_ = init_map
        self.in_game = True
        self.fps = fps
        self.t = None
    
    def update(self, input_):
        if input_ == 'w':
            self.map_.move([0, -1])
        if input_ == 'a':
            self.map_.move([-1, 0])
        if input_ == 's':
            self.map_.move([0, 1])
        if input_ == 'd':
            self.map_.move([1, 0])
    
    def main_thread(self):
        while self.in_game:
            self.map_.show()
            time.sleep(1/self.fps)
            os.system('cls' if os.name == 'nt' else 'clear')
        print('Bye!')
    
    def start_game(self):
        self.t = threading.Thread(target=self.main_thread)
        self.t.start()
        while True:
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

    def add_player(self, posi):
        if posi[0] <= self.col and posi[1] <= self.row: 
            self.player = agent('P', posi)
    
    def is_valid(self, posi):
        if posi[0] <= self.col and posi[1] <= self.row:
            if self.map_[posi[1]][posi[0]] == ' ':
                return True
            else:
                return False
    
    def move(self, direction, ag=None):
        if ag is None:
            ag = self.player
        new_posi = [ag.posi[0]+direction[0], ag.posi[1]+direction[1]]
        if self.is_valid(new_posi):
            ag.posi = new_posi
    
    def show(self):
        temp_map = copy.deepcopy(self.map_)
        temp_map[self.player.posi[1]][self.player.posi[0]] = 'P'
        for row in temp_map:
            print(' '.join(row))

class agent:
    def __init__(self, name, init_posi):
        self.posi = init_posi
        self.name = name

if __name__ == '__main__':
    b = Map(5, 5)
    b.add_player([2, 2])

    game = Game(b)
    game.start_game()
