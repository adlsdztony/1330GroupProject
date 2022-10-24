import os
import time
import threading

b = [''.join(['#' for i in range(10)]),
    '        '.join(['#' for i in range(2)]),
    ''.join(['#' for i in range(10)])]

FPS = 10
in_game = True
def board():
    while in_game:
        for j in b:
            print(j)
        time.sleep(1/FPS)
        os.system('clear')
t = threading.Thread(target=board)
t.start()
while True:
    a = input()
    if a == 'E':
        in_game = False
        break
    b.append(a)



