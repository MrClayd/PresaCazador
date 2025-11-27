class CeldaBase:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def es_transitable(self, es_jugador=False):
        return False

class Muro(CeldaBase):
    imagen = None
    def __init__(self, i, j):
        super().__init__(i, j)

    def permite_jugador(self):
        return False

    def permite_enemigo(self):
        return False

    def color(self):
        return "black"
    
class Camino(CeldaBase):
    def es_transitable(self, es_jugador=False):
        return True

class Tunel(CeldaBase):
    imagen = None
    def __init__(self, i, j, salida=None):
        super().__init__(i, j)
        self.salida = salida

    def permite_jugador(self):
        return True

    def permite_enemigo(self):
        return False

    def usar(self, entidad):
        if self.salida:
            entidad.i, entidad.j = self.salida

    def color(self):
        return "blue"

    def es_transitable(self, es_jugador=False):
        return True

    def usar(self, entidad):
        entidad.i, entidad.j = self.salida

class Liana(CeldaBase):
    imagen = None  

    def __init__(self, i, j, energia=20):
        super().__init__(i, j)
        self.energia = energia

    def permite_jugador(self):
        return False

    def permite_enemigo(self):
        return True

    def usar(self, jugador):
        jugador.energia = min(jugador.energia_max, jugador.energia + self.energia)

    def color(self):
        return "green"

class Salida(CeldaBase):
    def es_transitable(self, es_jugador=False):
        return True