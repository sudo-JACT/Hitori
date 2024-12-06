import os, sys
sys.path.append("../")



from libs.boardgame import BoardGame
from random import choice
from libs.boardgamegui import gui_play
from libs.datahandler import *
from libs.g2d import Point

class HitoriGame(BoardGame):
    
    def __init__(self, dim: Point, matrix: str) -> None:
        
        self._w, self._h = dim
        
        self._numbers = loadMatrix(matrix)
        self._annots = [0] * (self._w * self._h)
        
    
        

    def check_connection(self, x: int, y: int, c: int, mat_temp)->int:
    
        w, h =  self._w, self._h
        counter = c

        if (0 <= x < w and 0 <= y < h) and (mat_temp[x + y * w] == False) and (self._annots[x + y * w] != 1):

            counter += 1
            mat_temp[x + y * w] = True

            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:

                counter += self.check_connection(x + dx, y + dy, 0, mat_temp)
                
                
        return counter        



    def play(self, x: int, y: int, action) -> None:

        if action == "flag":
            
            if self._annots[x + y * self._w] == 0:
                
                self.fill(x, y)

            if self._annots[x + y * self._w] == 1:
                
                self.cross_circle(x, y)
            
            if self._annots[x + y * self._w] == 2:
                
                self.remove_clone(x, y)
                
        elif action == 666:
            
            self.automateH()
            
        elif action == "a":
            
            self.AI()
            
        else:

            self._annots[x + y * self._w] += 1
            self._annots[x + y * self._w] %= 3
        
        
            
        
    def analyze_move(self, x: int, y: int) -> None:
        
        w, h = self._w, self._h
        original_annots = self._annots[:]

        # Simula annerire
        self._annots[x + y * w] = 1
        self.automateH()
        if not self.wrong():
            black_result = self._annots[:]
        else:
            black_result = None
        self._annots = original_annots[:]  # Ripristina

        # Simula cerchiare
        self._annots[x + y * w] = 2
        self.automateH()
        if not self.wrong():
            circle_result = self._annots[:]
        else:
            circle_result = None
        self._annots = original_annots[:]  # Ripristina

        # Confronta i risultati
        if black_result and circle_result:
            if black_result == circle_result:
                print(f"Cella ({x}, {y}) può essere annerita o cerchiata.")  # Debug
            else:
                print(f"Ambiguità sulla cella ({x}, {y}).")  # Debug
        elif black_result:
            print(f"Annerimento sicuro per la cella ({x}, {y}).")  # Debug
            self._annots = black_result
        elif circle_result:
            print(f"Cerchiatura sicura per la cella ({x}, {y}).")  # Debug
            self._annots = circle_result
        else:
            print(f"Nessuna azione possibile per la cella ({x}, {y}).")  # Debug



    def AI(self) -> None:
        print("AI in esecuzione...")  # Debug
        w, h = self._w, self._h

        for y in range(h):
            for x in range(w):
                if self._annots[x + y * self._w] == 0:  # Solo celle non annotate
                    self.analyze_move(x, y)





    def automateH(self) -> None:
        
        for x in range(self._w):
            
            for y in range(self._h):
                
                if self._annots[x + y * self._w] == 1:
                    
                    self.cross_circle(x, y)
                    
                elif self._annots[x + y * self._w] == 2:
                    
                    self.remove_clone(x, y)


    def read(self, x: int, y: int) -> str:

        txt = str(self._numbers[x + y * self._w])

        if self._annots[x + y * self._w] == 1:

            txt += "#"

        elif self._annots[x + y * self._w] == 2:

            txt += "!"

        return txt


    def fill(self, x: int, y: int) -> None:

        bd, w, h = self._annots, self._w, self._h

        if 0 <= x < w and 0 <= y < h and bd[x + y * w] == 0:

            bd[x + y * w] = 1

            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:

                self.fill(x + dx, y + dy)


    def cross_circle(self, x: int, y: int) -> None:
                
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            
            if (0 <= (x+dx) < self._w and 0 <= (y+dy) < self._h) :
            
                self._annots[ (x+dx) + (y+dy) * self._w] = 2


    
    def remove_clone(self, x: int, y: int) -> None:
    
        for dx in range(self._w) :
            
            if self._numbers[x + y * self._w] == self._numbers[dx + y * self._w] and not (dx==x):

                self._annots[dx + y * self._w]=1

    
        for dy in range(self._h) :
            
            if self._numbers[x + y * self._w] == self._numbers[x + dy * self._w] and not (dy==y):

                self._annots[x + dy * self._w]=1
        


    def wrong(self) -> bool:
    
        # Controlla solo se ci sono numeri duplicati nelle righe e colonne ignorando i numeri anneriti
        for x in range(self._w):
            row_seen = set()
            col_seen = set()
            for y in range(self._h):
                # Controllo riga
                num = self._numbers[x + y * self._w]
                if self._annots[x + y * self._w] != 1:  # Ignora le celle annerite
                    if num in row_seen:
                        return True
                    row_seen.add(num)

                # Controllo colonna
                num = self._numbers[y + x * self._w]
                if self._annots[y + x * self._w] != 1:  # Ignora le celle annerite
                    if num in col_seen:
                        return True
                    col_seen.add(num)

        # Non verifica connessioni o celle nere adiacenti
        return False



    def finished(self) -> bool: 
        
        mat_temp = [False] * ( self._w * self._h)
        
        for x in range(self._w):
            
            for y in range(self._h):
                
                for z in range(self._h):
                    
                    try:
                    
                        if (self._numbers[x + y * self._w] == self._numbers[x + z * self._w]) and (z > y) and ((self._annots[x + y * self._w] != 1) and (self._annots[x + z * self._w] != 1)):
                            
                            return False
                            
                    except:
                        
                        pass
                    
                    try:
                        
                        if (self._numbers[x + y * self._w] == self._numbers[z + y * self._w]) and (x != z) and ((self._annots[x + y * self._w] != 1) and (self._annots[z + y * self._w] != 1)):
                            
                            return False
                        
                    except:
                        
                        pass
                
                
                try:
                    
                    if (self._annots[x + y * self._w] == 1 and self._annots[(x+1) + y * self._w] == 1) and self._w % (x+1) != 0:    
                        
                        return False
                
                except:
                    
                    pass
                
                
                try:
                    
                    if (self._annots[x + y * self._w] == 1 and self._annots[(x-1) + y * self._w] == 1)  and self._w % x == 0:
                        
                        return False
                
                except:
                    
                    pass
                
                
                try:
                    
                    if (self._annots[x + y * self._w] == 1 and self._annots[x + (y+1) * self._w] == 1) and self._y % (y+1) != 0:
                        
                        return False
                
                except:
                    
                    pass
                
                
                try:
                    
                    if (self._annots[x + y * self._w] == 1 and self._annots[x + (y-1) * self._w] == 1) and self._h % y == 0:
                        
                        return False
                
                except:
                    
                    pass

        f = False

        n = 0

        for x in range(self._w):
            
            for y in range(self._h):
                
                if (self._annots[x + y * self._w] == 0 or self._annots[x + y * self._w] == 2) and not(f):
                    
                    f = True
                                        
                    n = self.check_connection(x, y, n, mat_temp)
                    
        nt = self._annots.count(0) + self._annots.count(2)
        
        if n != nt:
            
            return False
        
        return True

    
    def status(self):
        
        return "Playing"

    
    def cols(self) -> int: 
        
        return self._w

    
    def rows(self) -> int: 
        
        return self._h








        
        
        
if __name__ == "__main__":
    
    hi = HitoriGame(6, 6)
    
    gui_play(hi)