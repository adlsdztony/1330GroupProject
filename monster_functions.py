from random import randint
from config import FPS, MONSTER_SPEED


def CatchOrRandom(around, state):
    if state % (FPS//MONSTER_SPEED) != 0:
        return [0, 0]
    for i, row in enumerate(around):
        if 'P' in row:
            return [row.index('P')-1 , i-1]
    return [randint(-1, 1), randint(-1, 1)]

def CatchOrStay(around, state):
    if state % (FPS//MONSTER_SPEED) != 0:
        return [0, 0]
    for i, row in enumerate(around):
        if 'P' in row:
            return [row.index('P')-1 , i-1]
    return [0, 0]

    
MONSTERS = {'M': CatchOrRandom, 'S': CatchOrStay}

if __name__ == '__main__':
    around = [
        [' ', ' ', 'P'],
        [' ', 'M', ' '],
        [' ', ' ', ' ']
    ]
    print(CatchOrRandom(around))