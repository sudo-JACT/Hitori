import os, sys
sys.path.append("../")



from libs.boardgame import *
from random import choice


intMatrix = list[list[int]]
anyMatrix = list[list[any]]

class HitoriGame(BoardGame):
    
    def __init__(self) -> None:
        
        self._m = None
        
        
    def initMatrix(self, d: int) -> intMatrix:
        
        l = [x for x in range(d+1)]
        l.pop(0)
        
        m = [[] for x in range(d)]
        
        
        for i in m:
            
            for j in range(d):
            
                x = choice(l)
                
                if i.count(x) <= 1:
                
                    i.append(x) # usare count per vedere se si ripete 2 volte se si non mettere altrimenti metti
        
        
        self._m = m
        
            
            
    def printM(self) -> None:
        
        for i in self._m:
            
            for j in i:
                
                print(j, end=" ")
                
            print("")
        
        
        
if __name__ == "__main__":
    
    hi = HitoriGame()
    
    hi.initMatrix(5)
    
    hi.printM()