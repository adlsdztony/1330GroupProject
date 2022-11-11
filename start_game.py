from engine import *
from maps import MAPS


def levels():
    for n, m in MAPS.items():
        g = Game(Map(m))
        print(n)
        g.map_.ShowMap()
        choice = input('press "Enter" to start\n"E + Enter" to exit')
        if choice == 'E':
            return 'exit'
        if g.start_game() == 'dead':
            return f'dead in {n}'
    return 'win'

while True:
    choice = input('press "Enter" to start\npress "E + Enter" to exit')
    if choice == 'E':
        break
    levels()