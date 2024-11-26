from libs.g2d import *
from libs.actor import *

class BoardGame(Arena):
    
    def __init__(self, size: Point):
        
        super().__init__(size)
        
        self._board = []
        
        for i in range(size[0]):
            
            self._board.append([])
            
            for j in range(size[1]):
                
                self._board[i].append(0)
                
                
    def printBoardinTerminal(self):
        
        for i in range(len(self._board)):
            
            for j in range(len(self._board[i])):
                
                print(self._board[i][j], end=" ")
                
            print("")