
    


import sys
import time
import random
import math
from threading import Thread
from datetime import datetime

''' Get key pressed without hitting Enter '''
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

snakeDirection = 'a'
snakePosition = []
snakeFood = [3, 4]
barrier = ['#', '#', '#', '#', '#', '#', '#', '#', '#', " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", '#', '#', '#', '#', '#', '#', '#', '#', '#']
content1 = ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#']
content2 = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
stopSnake = False
coins = 0
slowSnake = 0
snakeSpeed = [0.8, 0.6, 0.45, 0.3, 0.2, 0.15, 0.1]
startSnakeTime = datetime.now()
extraLife = 0
respawn = False

def isSnakeStraight(snakePosition):
    if snakePosition[0][0] != snakePosition[1][0]:
        return False
    return True

def showSnakeBoard():
    while True:
        global stopSnake, snakeDirection, snakeFood, coins, startSnakeTime, snakeSpeed, extraLife, respawn, snakePosition
        
        if stopSnake:
            break
        
        ''' Show board '''
        board = []
        board.append(barrier.copy())
        for i in range(3):
            board.append(content1.copy())
        for i in range(4):
            board.append(content2.copy())
        for i in range(3):
            board.append(content1.copy())
        board.append(barrier.copy())
        
        board[snakeFood[1]][snakeFood[0]] = "*"
        
        ''' Show snake updated position '''
        tempList = []
        if snakeDirection == 'w':
            tempList.append(snakePosition[0][0])
            tempList.append(snakePosition[0][1]-1 if snakePosition[0][1]-1>=0 else len(board)-1)
            snakePosition.insert(0, tempList)
        elif snakeDirection == 'a':
            tempList.append(snakePosition[0][0]-1 if snakePosition[0][0]-1>=0 else len(board[0])-1)
            tempList.append(snakePosition[0][1])
            snakePosition.insert(0, tempList)
        elif snakeDirection == 's':
            tempList.append(snakePosition[0][0])
            tempList.append(snakePosition[0][1]+1 if snakePosition[0][1]+1<len(board) else 0)
            snakePosition.insert(0, tempList)
        elif snakeDirection == 'd':
            tempList.append(snakePosition[0][0]+1 if snakePosition[0][0]+1<len(board[0]) else 0)
            tempList.append(snakePosition[0][1])
            snakePosition.insert(0, tempList)
        
        ''' Check if snake length needs +1 '''
        food = False
        if snakePosition[0] == snakeFood:
            food = True
            for i in range(len(snakePosition)):
                board[snakePosition[i][1]][snakePosition[i][0]] = '·'
        else:
            ''' Remove snake tail and add snake to board '''
            snakePosition.pop()
            for i in range(1, len(snakePosition)):
                board[snakePosition[i][1]][snakePosition[i][0]] = '·'
        
            if board[snakePosition[0][1]][snakePosition[0][0]] == '#' or board[snakePosition[0][1]][snakePosition[0][0]] == '·':
                if extraLife == 0:
                    print("\nYou lose")
                    print("\nPress any button to continue ...")
                    stopSnake = True
                    break
                else:
                    print("\nYou lose")
                    while len(snakePosition) > 140:
                        snakePosition.pop()
                    tempX = 10
                    tempY = 3
                    tempContinue = True
                    isRight = True
                    for i in range(len(snakePosition)):
                        if tempX == 30:
                            isRight = False
                            tempY += 1
                            tempX -= 1
                        elif tempX == 9:
                            isRight = True
                            tempY += 1
                            tempX += 1
                        
                        snakePosition[i][0] = tempX
                        snakePosition[i][1] = tempY
                        
                        if isRight: tempX += 1
                        else: tempX -= 1
                        
                    respawn = True
                    stopSnake = True
                    print("\nPress any button to continue ...")
                    break
        
        ''' Add snake head '''
        board[snakePosition[0][1]][snakePosition[0][0]] = '•'
        
        ''' Update coins & snake food position '''
        if food:
            coins += math.ceil(len(snakePosition)*0.3)
            tempRand1 = random.randint(0, len(board)-1)
            tempRand2 = random.randint(0, len(board[0])-1)
            while board[tempRand1][tempRand2] == '#' or board[tempRand1][tempRand2] == '·' or board[tempRand1][tempRand2] == '•':
                tempRand1 = random.randint(0, len(board)-1)
                tempRand2 = random.randint(0, len(board[0])-1)
            snakeFood = [tempRand2, tempRand1]
            board[tempRand1][tempRand2] = '*'
        
        ''' Print board '''
        output = ""
        output += "\n\n\n\n\n"
        output += printHeaderStatement() + "\n"
        for i in range(len(board)):
            output += "".join(board[i]) + "\n"
        
        print(output)
        
        if respawn:
            respawn = False
            print("\nGame is starting in 3")
            time.sleep(1)
            print("\nGame is starting in 2")
            time.sleep(1)
            print("\nGame is starting in 1")
            time.sleep(1)
        
        try:
            slowSnakeTime = snakeSpeed[int(((datetime.now()-startSnakeTime).total_seconds()+len(snakePosition))/25)]
            if slowSnakeTime <= 0.5:
                time.sleep(slowSnakeTime + slowSnake)
            else:
                time.sleep(slowSnakeTime)
        except:
            time.sleep(snakeSpeed[len(snakeSpeed)-1] + slowSnake)

def printHeaderStatement():
    lifeStatement = "Extra Life: " + "❤ x " + str(extraLife)
    coinStatement = "Coins: 💰 x " + str(coins)
    return lifeStatement + "     " + coinStatement + "\n"

def startSnake():
    global snakeDirection, stopSnake, snakePosition, startSnakeTime
    
    startSnakeTime = datetime.now()
    thread = Thread(target = showSnakeBoard)
    thread.start()
    
    while True:
        getch = getchar()
        if chr(ord(getch)) == 't':
            stopSnake = True
        elif chr(ord(getch)) == 'w' and not isSnakeStraight(snakePosition):
            snakeDirection = 'w'
        elif chr(ord(getch)) == 'a' and isSnakeStraight(snakePosition):
            snakeDirection = 'a'
        elif chr(ord(getch)) == 's' and not isSnakeStraight(snakePosition):
            snakeDirection = 's'
        elif chr(ord(getch)) == 'd' and isSnakeStraight(snakePosition):
            snakeDirection = 'd'
        if stopSnake:
            thread.join()
            break

def readySnake():
    global snakeDirection, snakePosition, snakeFood, stopSnake
    
    stopSnake = False
    snakeDirection = 'a'
    snakeFood = [3, 4]
    if not respawn:
        snakePosition = []
        snakePosition1 = [11, 6]
        snakePosition2 = [12, 6]
        snakePosition.append(snakePosition1.copy())
        snakePosition.append(snakePosition2.copy())
        print("\n\n\n\n\nSnake!!!\nPress WASD to control the snake\nPress t to end this game ...")
        time.sleep(1)
        
        print("\nGame is starting in 3")
        time.sleep(1)
        print("\nGame is starting in 2")
        time.sleep(1)
        print("\nGame is starting in 1")
        time.sleep(1)
    startSnake()

def shop():
    global slowSnake, coins, extraLife
    
    while True:
        print("\n\n\n\n\n" + printHeaderStatement())
        print("Shop - What do you want to buy ?\n")
        price = int(slowSnake*100+20*(1+slowSnake+0.25))
        choice = input("1: Slow Snake Speed - " + (str(slowSnake) if len(str(slowSnake))<=4 else str(slowSnake)[0:4]) + " (" + str(price) + " Coins)     2: Extra Life (1 coins)     3: Leave Shop\n")
        if choice == '1':
            if coins >= price:
                coins -= price
                slowSnake += 0.05
                print("\n\n\n\n\nSlow Snake bought !")
                time.sleep(1)
            else:
                print("\n\n\n\n\nNot enough coins! Play Snake to earn more coins!\n\nPress any button to go back ...")
                getch = getchar()
        elif choice == '2':
            if coins >= 1:
                coins -= 1
                extraLife += 1
                print("\n\n\n\n\nExtra life bought !")
                time.sleep(1)
            else:
                print("\n\n\n\n\nNot enough coins! Play Snake to earn more coins!\n\nPress any button to go back ...")
                getch = getchar()
        elif choice == '3':
            print("\n\n\n\n\n")
            break
        
def main():
    global respawn, extraLife
    
    games = ['p', '1', '2']
    choice = '-----------'
    
    print("Welcome to the snake world !!!")
    time.sleep(1)
    
    while True:
        if respawn:
            tempRespawn = "0"
            while tempRespawn != "y" and tempRespawn != "n":
                tempRespawn = input("\n\n\n\n\nRespawn ? (y/n)")
            if tempRespawn == "y":
                extraLife -= 1
                readySnake()
            else:
                respawn = False
        else:
            print("\n\n\n\n\n" + printHeaderStatement())
            choice = input("Please choose:\n\n1: Snake     2: Shop     p: Terminate Application\n")
    
            if choice == games[0]:
                print("Bye ~")
                break
            elif choice == games[1]:
                readySnake()
            elif choice == games[2]:
                shop()

main()
