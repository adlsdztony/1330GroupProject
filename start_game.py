from engine import *


b = Map(5, 5)
b.add_player([2, 2])

game = Game(b)
game.start_game()
