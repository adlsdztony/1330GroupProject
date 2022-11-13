from random import randint
from config import FPS, MONSTER_SPEED


def CatchOrRandom(around, state):
    if state % (FPS//MONSTER_SPEED[0]) != 0:
        return [0, 0]
    for i, row in enumerate(around):
        if 'P' in row:
            return [row.index('P')-1 , i-1]
    return [randint(-1, 1), randint(-1, 1)]

def CatchOrStay(around, state):
    if state % (FPS//MONSTER_SPEED[0]) != 0:
        return [0, 0]
    for i, row in enumerate(around):
        if 'P' in row:
            return [row.index('P')-1 , i-1]
    return [0, 0]

def Horizontal(around, state):
    if state % (FPS//MONSTER_SPEED[0]) == 0:
        if state // (FPS//MONSTER_SPEED[0]) % 4 >=2:
            return [1, 0]
        else:
            return [-1, 0]
    return [0, 0]

def Vertical(around, state):
    if state % (FPS//MONSTER_SPEED[0]) == 0:
        if state // (FPS//MONSTER_SPEED[0]) % 4 >=2:
            return [0, -1]
        else:
            return [0, 1]
    return [0, 0]
    
MONSTERS = {'M': CatchOrRandom, 'S': CatchOrStay, 'H': Horizontal, 'V': Vertical}

if __name__ == '__main__':
    around = [
        [' ', ' ', 'P'],
        [' ', 'M', ' '],
        [' ', ' ', ' ']
    ]
    state = 1
    print(CatchOrRandom(around, state))