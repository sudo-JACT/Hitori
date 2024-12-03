import os, sys
sys.path.append("../")



from libs.boardgame import BoardGame
from random import choice
from libs.boardgamegui import gui_play


class HitoriGame(BoardGame):
    
    def __init__(self, w: int, h: int) -> None:
        
        self._w, self._h = w, h
        self._numbers = list(range(w * h))
        self._annots = [0] * (w * h)
        

    def play(self, x, y, action) -> None:

        if action == "flag":

            self.fill(x, y)

        else:

            self._annots[x + y * self._w] += 1
            self._annots[x + y * self._w] %= 3


    def read(self, x: int, y: int) -> str:

        txt = str(self._numbers[x + y * self._w])

        if self._annots[x + y * self._w] == 1:

            txt += "#"

        elif self._annots[x + y * self._w] == 2:

            txt += "!"

        return txt


    def fill(self, x: int, y: int):

        bd, w, h = self._annots, self._w, self._h

        if 0 <= x < w and 0 <= y < h and bd[x + y * w] == 0:

            bd[x + y * w] = 1

            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:

                self.fill(x + dx, y + dy)


    def finished(self) -> bool: 
        
        for x in range(self._w):
            
            for y in range(self._h):
                
                for z in range(self._h):
                    
                    try:
                    
                        if self._numbers[x + y * self._w] == self._numbers[x + z * self._w] and z > y:
                            
                            print("CACCA")
                            
                            return False
                            
                    except:
                        
                        pass
                    
                    try:
                        
                        if self._numbers[x + y * self._w] == self._numbers[(x*5) + y * self._w]:
                            
                            print("CACCA2")
                            
                            return False
                        
                    except:
                        
                        pass
                
                
                try:
                    
                    if (self._annots[x + y * self._w] == 1 and self._annots[(x+1) + y * self._w] == 1) and self._w % (x+1) != 0:
                        
                        print("LOL")
                        
                        return False
                
                except:
                    
                    pass
                
                
                try:
                    
                    if (self._annots[x + y * self._w] == 1 and self._annots[(x-1) + y * self._w] == 1)  and self._w % x == 0:
                        
                        print("LMAO")
                        
                        return False
                
                except:
                    
                    pass
                
                
                try:
                    
                    if (self._annots[x + y * self._w] == 1 and self._annots[x + (y+1) * self._w] == 1):
                        
                        print("XD")
                        
                        return False
                
                except:
                    
                    pass
                
                
                try:
                    
                    if (self._annots[x + y * self._w] == 1 and self._annots[x + (y-1) * self._w] == 1):
                        
                        print(":)")
                        
                        return False
                
                except:
                    
                    pass

        
        return False

    
    def status(self):
        
        return "Playing"

    
    def cols(self) -> int: 
        
        return self._w

    
    def rows(self) -> int: 
        
        return self._h
        
        
        
if __name__ == "__main__":
    
    hi = HitoriGame(6, 6)
    
    gui_play(hi)