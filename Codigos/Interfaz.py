import tkinter as tk
import time
from Mapa import tipo_de_celda, CAMINO
from Entidades import Jugador, Enemigo
from trampas import Trampa
from pathfinding import bfs, astar

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

        # Enemigo inicial
        self.enemigo = Enemigo(10, 10)  # posición de prueba
        self.enemigo_sprite = self.canvas.create_rectangle(
            10*self.cell_size+5, 10*self.cell_size+5,
            10*self.cell_size+self.cell_size-5, 10*self.cell_size+self.cell_size-5,
            fill="yellow", tags="enemigo"
        )

        # Trampas
        self.trampas = []
        self.ultimo_colocada = 0

        # Bind de teclas
        self.root.bind("<Up>", lambda e: self.mover_jugador(-1, 0))
        self.root.bind("<Down>", lambda e: self.mover_jugador(1, 0))
        self.root.bind("<Left>", lambda e: self.mover_jugador(0, -1))
        self.root.bind("<Right>", lambda e: self.mover_jugador(0, 1))
        self.root.bind("<space>", lambda e: self.colocar_trampa())  # espacio para colocar trampa

        self.mover_enemigo()

    def dibujar_mapa(self):
        alto, ancho = len(self.mapa), len(self.mapa[0])
        for i in range(alto):
            for j in range(ancho):
                celda = tipo_de_celda(self.mapa[i][j])
                x1, y1 = j*self.cell_size, i*self.cell_size
                x2, y2 = x1+self.cell_size, y1+self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=celda.color(), outline="black")

    def mover_jugador(self, di, dj):
        if self.jugador.mover(di, dj, self.mapa, es_jugador=True):
            i, j = self.jugador.posicion()
            x1, y1 = j*self.cell_size+5, i*self.cell_size+5
            x2, y2 = x1+self.cell_size-10, y1+self.cell_size-10
            self.canvas.coords(self.jugador_sprite, x1, y1, x2, y2)

    def colocar_trampa(self):
        ahora = time.time()
        if len(self.trampas) < 3 and (ahora - self.ultimo_colocada) >= 5:
            i, j = self.jugador.posicion()
            if self.mapa[i][j] == CAMINO:  # solo en caminos
                trampa = Trampa(i, j)
                self.trampas.append(trampa)
                self.ultimo_colocada = ahora
                # Dibujar trampa
                trampa.id == self.canvas.create_rectangle(
                    j*self.cell_size+10, i*self.cell_size+10,
                    j*self.cell_size+self.cell_size-10, i*self.cell_size+self.cell_size-10,
                    fill="brown"
                )

    def mover_enemigo(self):
        ji, jj = self.jugador.posicion()
        ei, ej = self.enemigo.posicion()

        di, dj = bfs(self.mapa, (ei, ej), (ji, jj), es_jugador=False)

        if self.enemigo.mover(di, dj, self.mapa, es_jugador=False):
            ei, ej = self.enemigo.posicion()
            x1, y1 = ej*self.cell_size+5, ei*self.cell_size+5
            x2, y2 = x1+self.cell_size-10, y1+self.cell_size-10
            self.canvas.coords(self.enemigo_sprite, x1, y1, x2, y2)

        # Verificar colisión con trampas
        for trampa in list(self.trampas):
            if (ei, ej) == trampa.posicion():
                print("¡Enemigo atrapado por trampa!")
                self.trampas.delete(trampa.id)
                self.canvas.remove(trampa)
                self.canvas.delete(self.enemigo_sprite)
                # Respawn enemigo en 10 segundos
                self.root.after(10000, self.respawn_enemigo)

        self.root.after(500, self.mover_enemigo)

    def respawn_enemigo(self):
        # Reaparece en posición fija o aleatoria
        self.enemigo = Enemigo(10, 10)
        self.enemigo_sprite = self.canvas.create_rectangle(
            10*self.cell_size+5, 10*self.cell_size+5,
            10*self.cell_size+self.cell_size-5, 10*self.cell_size+self.cell_size-5,
            fill="yellow", tags="enemigo"
        )