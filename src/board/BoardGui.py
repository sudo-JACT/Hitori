from libs.g2d import *
from libs.actor import *
from board.BoardGame import *

class BoardGui():
    
    def __init__(self, size: Point) -> None:
        
        self._size = size
        self._game = BoardGame(size)
        
        
    def printMaskinTerminal(self):
        
        self._game.printBoardinTerminal()