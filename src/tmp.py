import random

# 1. Funzione per creare una griglia di base
def crea_griglia_base(dim):
    return [[random.randint(1, dim) for _ in range(dim)] for _ in range(dim)]

# 2. Funzione per verificare se la griglia è valida
def è_valida(griglia):
    return (nessun_numero_duplicato(griglia) and 
            nessuna_cella_annerita_adiacente(griglia) and 
            celle_connesse(griglia))

# 3. Controllo per numeri duplicati
def nessun_numero_duplicato(griglia):
    # Per ogni riga e colonna, controlla duplicati tra numeri non anneriti
    for riga in griglia:
        numeri_visti = set()
        for numero in riga:
            if numero != 'X' and numero in numeri_visti:  # 'X' rappresenta una cella annerita
                return False
            numeri_visti.add(numero)
    # Ripeti per colonne
    for colonna in zip(*griglia):
        numeri_visti = set()
        for numero in colonna:
            if numero != 'X' and numero in numeri_visti:
                return False
            numeri_visti.add(numero)
    return True

# 4. Controllo celle annerite adiacenti
def nessuna_cella_annerita_adiacente(griglia):
    dim = len(griglia)
    for i in range(dim):
        for j in range(dim):
            if griglia[i][j] == 'X':  # Se la cella è annerita
                # Controlla celle adiacenti
                if i > 0 and griglia[i-1][j] == 'X': return False  # Sopra
                if i < dim-1 and griglia[i+1][j] == 'X': return False  # Sotto
                if j > 0 and griglia[i][j-1] == 'X': return False  # Sinistra
                if j < dim-1 and griglia[i][j+1] == 'X': return False  # Destra
    return True

# 5. Controllo connessione celle non annerite
def celle_connesse(griglia):
    dim = len(griglia)
    visitate = [[False for _ in range(dim)] for _ in range(dim)]

    # Trova una cella non annerita per iniziare la ricerca
    def trova_prima_cella():   
        for i in range(dim):
            for j in range(dim):
                if griglia[i][j] != 'X':
                    return (i, j)
        return None

    def dfs(x, y):
        # Fuori dai limiti o già visitata o annerita
        if x < 0 or y < 0 or x >= dim or y >= dim or visitate[x][y] or griglia[x][y] == 'X':
            return
        visitate[x][y] = True
        # Visita celle adiacenti
        dfs(x+1, y)
        dfs(x-1, y)
        dfs(x, y+1)
        dfs(x, y-1)

    partenza = trova_prima_cella()
    if not partenza: return True  # Se tutte le celle sono annerite
    dfs(partenza[0], partenza[1])

    # Controlla se ci sono celle non annerite non visitate
    for i in range(dim):
        for j in range(dim):
            if griglia[i][j] != 'X' and not visitate[i][j]:
                return False
    return True

# 6. Funzione principale
def genera_hitori(dim):
    griglia = crea_griglia_base(dim)
    while not è_valida(griglia):
        # Prova a risolvere annerendo alcune celle (qui puoi implementare logica più avanzata)
        for i in range(dim):
            for j in range(dim):
                if random.random() < 0.2:  # Prova ad annerire il 20% delle celle casualmente
                    griglia[i][j] = 'X'
    return griglia

# Test del sistema
dim = 5
griglia = genera_hitori(dim)
for riga in griglia:
    print(" ".join(str(cell) for cell in riga))
