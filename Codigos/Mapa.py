import random
from collections import deque

CAMINO = 0
LIANA  = 1
TUNEL  = 2
MURO   = 3
SALIDA = 4

class CeldaBase:
    def __init__(self, tipo):
        self.tipo = tipo

    def permite_jugador(self):
        return self.tipo in (CAMINO, TUNEL, SALIDA)

    def permite_enemigo(self):
        return self.tipo in (CAMINO, LIANA)

    def color(self):
        return {
            CAMINO: "lightgray",
            LIANA: "green",
            TUNEL: "blue",
            MURO: "black",
            SALIDA: "gold"
        }[self.tipo]

class Camino(CeldaBase): 
    def __init__(self): 
        super().__init__(CAMINO)
class Liana(CeldaBase):   
    def __init__(self): 
        super().__init__(LIANA)
class Tunel(CeldaBase):   
    def __init__(self):
        super().__init__(TUNEL)
class Muro(CeldaBase):    
    def __init__(self):
        super().__init__(MURO)
class Salida(CeldaBase):  
    def __init__(self): 
        super().__init__(SALIDA)

def tipo_de_celda(id_tipo):
    return {CAMINO: Camino, LIANA: Liana, TUNEL: Tunel, MURO: Muro, SALIDA: Salida}[id_tipo]()

def generar_mapa(ancho=10, alto=10):
    while True:
        mapa = [[CAMINO for _ in range(ancho)] for _ in range(alto)]

        # Bordes como muros
        for i in range(alto):
            for j in range(ancho):
                if i == 0 or j == 0 or i == alto-1 or j == ancho-1:
                    mapa[i][j] = MURO

        # Obstáculos internos
        total = (ancho-2) * (alto-2)
        num_muros   = random.randint(int(total*0.15), int(total*0.25))
        num_lianas  = random.randint(int(total*0.05), int(total*0.10))
        num_tuneles = random.randint(int(total*0.05), int(total*0.10))

        def colocar(tipo, cantidad):
            c = 0
            while c < cantidad:
                i, j = random.randrange(1, alto-1), random.randrange(1, ancho-1)
                if mapa[i][j] == CAMINO:
                    mapa[i][j] = tipo
                    c += 1

        colocar(MURO, num_muros)
        colocar(LIANA, num_lianas)
        colocar(TUNEL, num_tuneles)

        inicio = (1, 1)
        mapa[inicio[0]][inicio[1]] = CAMINO

        salida = (alto-2, ancho-2)
        mapa[salida[0]][salida[1]] = SALIDA

        if hay_camino_valido(mapa, inicio, salida):
            return mapa, inicio, salida

def hay_camino_valido(mapa, inicio, salida):
    alto, ancho = len(mapa), len(mapa[0])
    q = deque([inicio])
    visit = {inicio}
    while q:
        i, j = q.popleft()
        if (i, j) == salida:
            return True
        for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
            ni, nj = i+di, j+dj
            if 0 <= ni < alto and 0 <= nj < ancho:
                if mapa[ni][nj] in (CAMINO, TUNEL, SALIDA) and (ni, nj) not in visit:
                    visit.add((ni, nj))
                    q.append((ni, nj))
    return False