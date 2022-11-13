from engine import *
from maps import MAPS
import os


def levels():
    for n, m in MAPS.items():
        g = Game(Map(m))
        os.system(clear)
        print(n)
        g.map_.ShowMap()
        print('press any keys to start\n"E" to exit\n')
        choice = chr(ord(getchar()))
        if choice == 'E':
            return 'exit'
        state = g.start_game()
        if state == 'dead':
            return f'dead in {n}'
        if state == 'exit':
            return 'exit'
    return 'win'

def print_help():
    os.system(clear)
    with open('readme.txt') as readme:
        for line in readme.readlines():
            print(line, end='')
            if 'Enjoy' in line:
                break
        print('(read more in readme.txt)')
    print('press any keys to continue')
    getchar()


while True:
    os.system(clear)
    print(f'Speed now: {MONSTER_SPEED[0]}\n1. press any keys to start\n2. press "H" to read help\n3. press "E" to exit\n')
    choice = chr(ord(getchar()))
    if choice == 'E':
        break
    if choice == 'H':
        print_help()
        continue
    if levels() == 'win':
        MONSTER_SPEED[0] += 1
        print(f'Speed up!')