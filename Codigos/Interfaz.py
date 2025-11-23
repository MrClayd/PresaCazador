import tkinter as tk
import time
import random
from Mapa import tipo_de_celda, CAMINO, LIANA
from Entidades import Jugador, Enemigo
from trampas import Trampa
from Energia import Energia
from pathfinding import bfs

class Interfaz:
    def __init__(self, root, mapa, inicio, salida):
        self.root = root
        self.mapa = mapa
        self.cell_size = 40

        alto, ancho = len(mapa), len(mapa[0])
        self.canvas = tk.Canvas(root, width=ancho*self.cell_size, height=alto*self.cell_size)
        self.canvas.pack()

        self.dibujar_mapa()

        # Jugador
        self.jugador = Jugador(*inicio)
        self.jugador_sprite = self.canvas.create_oval(
            inicio[1]*self.cell_size+5, inicio[0]*self.cell_size+5,
            inicio[1]*self.cell_size+self.cell_size-5, inicio[0]*self.cell_size+self.cell_size-5,
            fill="red", tags="jugador"
        )

        # Enemigos iniciales
        self.enemigos = []
        posiciones_generadas = set()
        intentos = 0
        while len(posiciones_generadas) < 3 and intentos < 500:
            intentos += 1
            i = random.randrange(1, alto-1)
            j = random.randrange(1, ancho-1)
            if (i, j) != tuple(inicio) and (i, j) not in posiciones_generadas and self.mapa[i][j] in (CAMINO, LIANA):
                posiciones_generadas.add((i, j))

        for (i, j) in posiciones_generadas:
            enemigo = Enemigo(i, j)
            sprite = self.canvas.create_rectangle(
                j*self.cell_size+5, i*self.cell_size+5,
                j*self.cell_size+self.cell_size-5, i*self.cell_size+self.cell_size-5,
                fill="yellow", tags="enemigo"
            )
            self.enemigos.append([enemigo, sprite])

        # Trampas
        self.trampas = []
        self.ultimo_colocada = 0

        # Energía
        self.energia = Energia(max_energia=10)
        self.ultimo_movimiento = 0
        self.cooldown = 1  # segundos

        # Barra de energía
        self.energia_bar = tk.Canvas(root, width=200, height=20, bg="gray")
        self.energia_bar.pack(pady=5)
        self.actualizar_barra_energia()

        # Bind de teclas
        self.root.bind("<Up>", lambda e: self.mover_jugador(-1, 0, correr=False))
        self.root.bind("<Down>", lambda e: self.mover_jugador(1, 0, correr=False))
        self.root.bind("<Left>", lambda e: self.mover_jugador(0, -1, correr=False))
        self.root.bind("<Right>", lambda e: self.mover_jugador(0, 1, correr=False))
        self.root.bind("<Shift-Up>", lambda e: self.mover_jugador(-1, 0, correr=True))
        self.root.bind("<Shift-Down>", lambda e: self.mover_jugador(1, 0, correr=True))
        self.root.bind("<Shift-Left>", lambda e: self.mover_jugador(0, -1, correr=True))
        self.root.bind("<Shift-Right>", lambda e: self.mover_jugador(0, 1, correr=True))
        self.root.bind("<space>", lambda e: self.colocar_trampa())

        self.mover_enemigo()

    def dibujar_mapa(self):
        alto, ancho = len(self.mapa), len(self.mapa[0])
        for i in range(alto):
            for j in range(ancho):
                celda = tipo_de_celda(self.mapa[i][j])
                x1, y1 = j*self.cell_size, i*self.cell_size
                x2, y2 = x1+self.cell_size, y1+self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=celda.color(), outline="black")

    def actualizar_barra_energia(self):
        self.energia_bar.delete("all")
        porcentaje = self.energia.actual / self.energia.max_energia
        ancho = int(200 * porcentaje)
        color = "green" if porcentaje > 0.5 else "orange" if porcentaje > 0.2 else "red"
        self.energia_bar.create_rectangle(0, 0, ancho, 20, fill=color)

    def mover_jugador(self, di, dj, correr=False):
        ahora = time.time()
        if ahora - self.ultimo_movimiento < self.cooldown:
            return

        if correr:
            if not self.energia.consumir(2):
                print("Sin energía para correr")
                return
            di *= 2
            dj *= 2

        if self.jugador.mover(di, dj, self.mapa, es_jugador=True):
            i, j = self.jugador.posicion()
            x1, y1 = j*self.cell_size+5, i*self.cell_size+5
            x2, y2 = x1+self.cell_size-10, y1+self.cell_size-10
            self.canvas.coords(self.jugador_sprite, x1, y1, x2, y2)

        self.ultimo_movimiento = ahora
        self.energia.regenerar()
        self.actualizar_barra_energia()

    def colocar_trampa(self):
        ahora = time.time()
        if len(self.trampas) < 3 and (ahora - self.ultimo_colocada) >= 5:
            i, j = self.jugador.posicion()
            if self.mapa[i][j] == CAMINO:
                trampa = Trampa(i, j)
                self.trampas.append(trampa)
                self.ultimo_colocada = ahora
                trampa.id = self.canvas.create_rectangle(
                    j*self.cell_size+10, i*self.cell_size+10,
                    j*self.cell_size+self.cell_size-10, i*self.cell_size+self.cell_size-10,
                    fill="brown"
                )

    def mover_enemigo(self):
        if not self.enemigos:
            self.root.after(500, self.mover_enemigo)
            return

        posiciones_ocupadas = {enemigo.posicion() for enemigo, _ in self.enemigos}
        ji, jj = self.jugador.posicion()

        for enemigo_data in list(self.enemigos):
            enemigo, sprite = enemigo_data
            ei, ej = enemigo.posicion()
            di, dj = bfs(self.mapa, (ei, ej), (ji, jj), es_jugador=False)
            nuevo_i, nuevo_j = ei + di, ej + dj

            alto, ancho = len(self.mapa), len(self.mapa[0])
            if not (0 <= nuevo_i < alto and 0 <= nuevo_j < ancho):
                continue
            if (nuevo_i, nuevo_j) in posiciones_ocupadas:
                continue

            posiciones_ocupadas.discard((ei, ej))
            if enemigo.mover(di, dj, self.mapa, es_jugador=False):
                posiciones_ocupadas.add((nuevo_i, nuevo_j))
                ei, ej = enemigo.posicion()
                x1, y1 = ej*self.cell_size+5, ei*self.cell_size+5
                x2, y2 = x1+self.cell_size-10, y1+self.cell_size-10
                self.canvas.coords(sprite, x1, y1, x2, y2)

                for trampa in list(self.trampas):
                    if (ei, ej) == trampa.posicion():
                        print("¡Enemigo atrapado por trampa!")
                        self.canvas.delete(trampa.id)
                        self.trampas.remove(trampa)
                        self.mapa[ei][ej] = CAMINO
                        self.canvas.delete(sprite)
                        self.enemigos.remove(enemigo_data)
                        self.root.after(10000, self.respawn_enemigo)
                        break  # salir del bucle de trampas

        self.root.after(500, self.mover_enemigo)


    def respawn_enemigo(self):
        if len(self.enemigos) >= 3:
            return
        
        alto, ancho = len(self.mapa), len(self.mapa[0])
        ji, jj = self.jugador.posicion()

        for _ in range(300):
            i = random.randrange(1, alto-1)
            j = random.randrange(1, ancho-1)
            # validar que la celda sea transitable y no esté ocupada por jugador ni por otro enemigo
            ocupada = False
            for e, _ in self.enemigos:
                if (i, j) == e.posicion():
                    ocupada = True
                    break
            if ocupada or (i, j) == (ji, jj):
                continue
            if self.mapa[i][j] in (CAMINO, LIANA):
                enemigo = Enemigo(i, j)
                sprite = self.canvas.create_rectangle(
                    j*self.cell_size+5, i*self.cell_size+5,
                    j*self.cell_size+self.cell_size-5, i*self.cell_size+self.cell_size-5,
                    fill="yellow", tags="enemigo"
                )
                self.enemigos.append([enemigo, sprite])
                return
        # Si no encontró sitio en X intentos, no hacer nada (evita crash)
        print("Aviso: no se pudo respawnear enemigo; mapa demasiado lleno.")
                