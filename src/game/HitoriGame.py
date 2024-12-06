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
            
        
    def AI(self) -> None:

        print("AI in esecuzione...")  # Debug
        w, h = self._w, self._h
        numbers = self._numbers
        annots = self._annots

        # Gestione delle righe
        for y in range(h):
            print(f"Controllo riga {y}")  # Debug
            row_counts = {}
            for x in range(w):
                num = numbers[x + y * w]
                if annots[x + y * w] == 0:  # Solo se non è già oscurato o contrassegnato
                    row_counts[num] = row_counts.get(num, 0) + 1

            print(f"Conteggi riga {y}: {row_counts}")  # Debug

            # Oscura una copia per riga
            for x in range(w):
                num = numbers[x + y * w]
                if row_counts.get(num, 0) > 1 and annots[x + y * w] == 0:
                    print(f"Provo a oscurare {num} alla posizione ({x}, {y})")  # Debug
                    annots[x + y * w] = 1
                    if not self.wrong():  # Se non viola le regole, conferma
                        print(f"Oscuro {num} alla posizione ({x}, {y})")  # Debug
                        row_counts[num] -= 1
                    else:  # Altrimenti ripristina
                        print(f"Ripristino {num} alla posizione ({x}, {y})")  # Debug
                        annots[x + y * w] = 0

        # Gestione delle colonne
        for x in range(w):
            print(f"Controllo colonna {x}")  # Debug
            col_counts = {}
            for y in range(h):
                num = numbers[x + y * w]
                if annots[x + y * w] == 0:  # Solo se non è già oscurato o contrassegnato
                    col_counts[num] = col_counts.get(num, 0) + 1

            print(f"Conteggi colonna {x}: {col_counts}")  # Debug

            # Oscura una copia per colonna
            for y in range(h):
                num = numbers[x + y * w]
                if col_counts.get(num, 0) > 1 and annots[x + y * w] == 0:
                    print(f"Provo a oscurare {num} alla posizione ({x}, {y})")  # Debug
                    annots[x + y * w] = 1
                    if not self.wrong():  # Se non viola le regole, conferma
                        print(f"Oscuro {num} alla posizione ({x}, {y})")  # Debug
                        col_counts[num] -= 1
                    else:  # Altrimenti ripristina
                        print(f"Ripristino {num} alla posizione ({x}, {y})")  # Debug
                        annots[x + y * w] = 0

        print(f"Annotazioni dopo l'AI: {annots}")  # Debug







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
        
        
    def show_state(self):
    
        for y in range(self._h):
            row = ""
            for x in range(self._w):
                num = self._numbers[x + y * self._w]
                ann = self._annots[x + y * self._w]
                if ann == 1:
                    row += f"[{num}] "  # Mostra la cella oscurata
                else:
                    row += f" {num}  "  # Mostra la cella non oscurata
            print(row)
        print("\n")  # Linea vuota tra le iterazioni per chiarezza

    def wrong(self) -> bool:
    
        print("Verifica stato...")
        w, h = self._w, self._h
        annots = self._annots
        numbers = self._numbers

        # Regola 1: Celle oscurate non devono essere adiacenti
        for x in range(w):
            for y in range(h):
                if annots[x + y * w] == 1:  # Se la cella è oscurata
                    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h and annots[nx + ny * w] == 1:
                            print(f"Errore: Celle adiacenti oscurate ({x}, {y}) e ({nx}, {ny})")  # Debug
                            return True

        # Regola 2: Numeri duplicati non oscurati nella stessa riga o colonna
        for y in range(h):
            seen = set()
            for x in range(w):
                if annots[x + y * w] == 0:  # Considera solo celle non oscurate
                    num = numbers[x + y * w]
                    if num in seen:
                        print(f"Errore: Duplicato non oscurato nella riga {y} per il numero {num}")  # Debug
                        return True
                    seen.add(num)

        for x in range(w):
            seen = set()
            for y in range(h):
                if annots[x + y * w] == 0:  # Considera solo celle non oscurate
                    num = numbers[x + y * w]
                    if num in seen:
                        print(f"Errore: Duplicato non oscurato nella colonna {x} per il numero {num}")  # Debug
                        return True
                    seen.add(num)

        # Regola 3: Tutte le celle non oscurate devono essere connesse
        mat_temp = [False] * (w * h)
        n = 0  # Numero di celle connesse trovate
        for x in range(w):
            for y in range(h):
                if annots[x + y * w] == 0:  # Trova una cella non oscurata
                    if n == 0:
                        # Avvia il conteggio delle connessioni
                        n = self.check_connection(x, y, n, mat_temp)
                    else:
                        # Trova un'altra componente non connessa
                        print(f"Errore: Celle non connesse rilevate a partire da ({x}, {y})")  # Debug
                        return True

        nt = annots.count(0)  # Conta tutte le celle non oscurate
        if n != nt:
            print(f"Errore: Numero celle connesse ({n}) diverso da totale non oscurate ({nt})")  # Debug
            return True

        # Nessun errore rilevato
        print("Stato valido.")  # Debug
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