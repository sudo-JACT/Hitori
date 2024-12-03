import os, sys
sys.path.append("../")



from libs.boardgame import BoardGame
from random import choice
from libs.boardgamegui import gui_play


intMatrix = list[list[int]]
anyMatrix = list[list[any]]

class HitoriGame(BoardGame):
    
    def __init__(self, w: int, h: int):
        
        self._w, self._h = w, h
        self._numbers = list(range(6 * 6))
        self._annots = [0] * (6 * 6)
        
        
    def play(self, x, y, action):
        if action == "flag":
            self.fill(x, y)
        else:
            self._annots[x + y * self._w] += 1
            self._annots[x + y * self._w] %= 3


    def read(self, x, y):
        txt = str(self._numbers[x + y * self._w])
        if self._annots[x + y * self._w] == 1:
            txt += "#"
        elif self._annots[x + y * self._w] == 2:
            txt += "!"
        return txt


    def fill(self, x, y):
        bd, w, h = self._annots, self._w, self._h
        if 0 <= x < w and 0 <= y < h and bd[x + y * w] == 0:
            bd[x + y * w] = 1
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                self.fill(x + dx, y + dy)

    
    def finished(self): 
        
        return False
    
    
    def status(self): 
        
        return "Playing"
    
    
    def cols(self): 
        
        return self._w
    
    
    def rows(self): 
        
        return self._h
        
        
        
if __name__ == "__main__":
    
    hi = HitoriGame(5, 5)
    
    gui_play(hi)