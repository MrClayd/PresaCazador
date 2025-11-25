from Mapa import Camino, Liana, Tunel, Salida

class EntidadBase:
    def __init__(self, i, j, velocidad=1):
        self.i = i  # fila
        self.j = j  # columna
        self.velocidad = velocidad

    def posicion(self):
        return self.i, self.j

    def mover(self, di, dj, mapa, es_jugador=False):
        ni, nj = self.i + di, self.j + dj
        alto, ancho = len(mapa), len(mapa[0])
        if 0 <= ni < alto and 0 <= nj < ancho:
            celda = mapa[ni][nj]
            if es_jugador and celda.permite_jugador():
                self.i, self.j = ni, nj
                # Acciones especiales
                if isinstance(celda, Tunel):
                    celda.usar(self)
                elif isinstance(celda, Liana):
                    celda.usar(self)
                return True
            elif not es_jugador and celda.permite_enemigo():
                self.i, self.j = ni, nj
                return True
        return False

class Jugador(EntidadBase):
    def __init__(self, i, j, energia_max=100):
        super().__init__(i, j, velocidad=1)
        self.energia_max = energia_max
        self.energia = energia_max
        self.corriendo = False

    def toggle_correr(self, activo):
        """Activa o desactiva el modo correr."""
        self.corriendo = activo if self.energia > 0 else False

    def tick_energia(self):
        """Actualiza la energía cada ciclo."""
        if self.corriendo:
            self.energia = max(0, self.energia - 5)
            if self.energia == 0:
                self.corriendo = False
        else:
            self.energia = min(self.energia_max, self.energia + 2)

    def velocidad_actual(self):
        return 2 if self.corriendo else 1

class Enemigo(EntidadBase):
    def __init__(self, i, j, velocidad=1):
        super().__init__(i, j, velocidad)
        self.vivo = True

    def matar(self):
        self.vivo = False

    def respawn(self, i, j):
        self.i, self.j = i, j
        self.vivo = True