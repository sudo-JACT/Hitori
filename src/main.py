from libs.boardgamegui import gui_play
from game.HitoriGame import *

if __name__ == "__main__":
    
    gui_play(HitoriGame(5, 5, "./tables/5-easy.csv"))