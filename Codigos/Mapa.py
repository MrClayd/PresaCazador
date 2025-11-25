import random
from collections import deque
from celdas import Muro, Camino, Tunel, Liana, Salida

class CeldaBase:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def permite_jugador(self):
        return False

    def permite_enemigo(self):
        return False

    def color(self):
        return "gray"  


class Camino(CeldaBase):
    def permite_jugador(self):
        return True

    def permite_enemigo(self):
        return True

    def color(self):
        return "lightgray"


class Liana(CeldaBase):
    def __init__(self, i, j, energia=20):
        super().__init__(i, j)
        self.energia = energia

    def permite_jugador(self):
        return False  # jugador no puede entrar en liana
    def permite_enemigo(self):
        return True

    def usar(self, jugador):
        jugador.energia = min(jugador.energia_max, jugador.energia + self.energia)

    def color(self):
        return "green"


class Tunel(CeldaBase):
    def __init__(self, i, j, salida=None):
        super().__init__(i, j)
        self.salida = salida  # coordenada de salida

    def permite_jugador(self):
        return True

    def permite_enemigo(self):
        return False

    def usar(self, entidad):
        if self.salida:
            entidad.i, entidad.j = self.salida

    def color(self):
        return "blue"


class Muro(CeldaBase):
    def permite_jugador(self):
        return False

    def permite_enemigo(self):
        return False

    def color(self):
        return "black"


class Salida(CeldaBase):
    def permite_jugador(self):
        return True

    def permite_enemigo(self):
        return True

    def color(self):
        return "gold"


# --- Generación de mapa ---
def generar_mapa(ancho=16, alto=16):
    while True:
        # Crear mapa inicial con objetos Camino
        mapa = [[Camino(i, j) for j in range(ancho)] for i in range(alto)]

        # Bordes como muros
        for i in range(alto):
            for j in range(ancho):
                if i == 0 or j == 0 or i == alto-1 or j == ancho-1:
                    mapa[i][j] = Muro(i, j)

        # Obstáculos internos
        total = (ancho-2) * (alto-2)
        num_muros   = random.randint(int(total*0.15), int(total*0.25))
        num_lianas  = random.randint(int(total*0.05), int(total*0.10))
        num_tuneles = random.randint(int(total*0.05), int(total*0.10))

        def colocar(factory, cantidad):
            c = 0
            while c < cantidad:
                i, j = random.randrange(1, alto-1), random.randrange(1, ancho-1)
                if isinstance(mapa[i][j], Camino):  # solo reemplazar caminos
                    mapa[i][j] = factory(i, j)
                    c += 1

        colocar(Muro, num_muros)
        colocar(Liana, num_lianas)
        colocar(Tunel, num_tuneles)

        inicio = (1, 1)
        mapa[inicio[0]][inicio[1]] = Camino(*inicio)

        salida = (alto-2, ancho-2)
        mapa[salida[0]][salida[1]] = Salida(*salida)

        if hay_camino_valido(mapa, inicio, salida):
            return mapa, inicio, salida


# --- Validación de camino ---
def hay_camino_valido(mapa, inicio, salida, es_jugador=True):
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
                celda = mapa[ni][nj]
                if (es_jugador and celda.permite_jugador()) or (not es_jugador and celda.permite_enemigo()):
                    if (ni, nj) not in visit:
                        visit.add((ni, nj))
                        q.append((ni, nj))
    return False