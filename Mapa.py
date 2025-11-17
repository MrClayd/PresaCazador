# Identificadores de celdas
CAMINO = 0
LIANA  = 1
TUNEL  = 2
MURO   = 3

class CeldaBase:
    def __init__(self, tipo):
        self.tipo = tipo

    def permite_jugador(self):
        return self.tipo in (CAMINO, TUNEL)

    def permite_enemigo(self):
        return self.tipo in (CAMINO, LIANA)

    def color(self):
        return {
            CAMINO: "lightgray",
            LIANA: "green",
            TUNEL: "blue",
            MURO: "black"
        }[self.tipo]

# Clases específicas de cada tipo de celda
class Camino(CeldaBase):
    def __init__(self): super().__init__(CAMINO)

class Liana(CeldaBase):
    def __init__(self): super().__init__(LIANA)

class Tunel(CeldaBase):
    def __init__(self): super().__init__(TUNEL)

class Muro(CeldaBase):
    def __init__(self): super().__init__(MURO)

def tipo_de_celda(id_tipo):
    return {CAMINO: Camino, LIANA: Liana, TUNEL: Tunel, MURO: Muro}[id_tipo]()