import random
from Mapa import generar_mapa, CAMINO, LIANA
from Entidades import Jugador, Enemigo
from pathfinding import hay_camino_enemigo   # usamos la validación que evita encierros

class Juego:
    def __init__(self, root, modo, dificultad, nombre_jugador, tam=(10, 10)):
        self.root = root
        self.modo_nombre = modo
        self.dificultad = dificultad
        self.nombre = nombre_jugador

        # Generar mapa aleatorio
        self.mapa = generar_mapa(tam[0], tam[1])

        # Jugador en inicio fijo (0,0)
        self.jugador = Jugador(0, 0)

        # Crear enemigos en posiciones válidas
        self.enemigos = self._crear_enemigos(dificultad)

    

    def _crear_enemigos(self, dificultad):
        """Coloca enemigos en posiciones aleatorias válidas."""
        num = {"facil": 2, "medio": 3, "dificil": 5}[dificultad]
        enemigos = []
        alto, ancho = len(self.mapa), len(self.mapa[0])

        for _ in range(num):
            while True:
                i, j = random.randrange(alto), random.randrange(ancho)
                # Solo en CAMINO o LIANA
                if self.mapa[i][j] in (CAMINO, LIANA):
                    # Validar que no esté encerrado
                    if hay_camino_enemigo(self.mapa, (i, j)):
                        enemigos.append(Enemigo(i, j))
                        break
        return enemigos