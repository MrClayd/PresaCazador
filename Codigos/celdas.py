class CeldaBase:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def es_transitable(self, es_jugador=False):
        return False

class Muro(CeldaBase):
    def es_transitable(self, es_jugador=False):
        return False

class Camino(CeldaBase):
    def es_transitable(self, es_jugador=False):
        return True

class Tunel(CeldaBase):
    def __init__(self, i, j, salida):
        super().__init__(i, j)
        self.salida = salida

    def es_transitable(self, es_jugador=False):
        return True

    def usar(self, entidad):
        entidad.i, entidad.j = self.salida

class Liana(CeldaBase):
    def __init__(self, i, j, energia=20):
        super().__init__(i, j)
        self.energia = energia

    def es_transitable(self, es_jugador=False):
        return True

    def usar(self, jugador):
        jugador.energia = min(jugador.energia_max, jugador.energia + self.energia)

class Salida(CeldaBase):
    def es_transitable(self, es_jugador=False):
        return True