import tkinter as tk
from Mapa import tipo_de_celda
from Entidades import Jugador

class Interfaz:
    def __init__(self, root, mapa):
        self.root = root
        self.mapa = mapa
        self.cell_size = 40  # tamaño de cada celda en píxeles

        # Canvas para dibujar
        alto, ancho = len(mapa), len(mapa[0])
        self.canvas = tk.Canvas(root, width=ancho*self.cell_size, height=alto*self.cell_size)
        self.canvas.pack()

        # Dibujar mapa
        self.dibujar_mapa()

        # Crear jugador en posición inicial (0,0)
        self.jugador = Jugador(0, 0)
        self.jugador_sprite = self.canvas.create_oval(
            5, 5, self.cell_size-5, self.cell_size-5,
            fill="red", tags="jugador"
        )

        # Bind de teclas
        self.root.bind("<Up>", lambda e: self.mover_jugador(-1, 0))
        self.root.bind("<Down>", lambda e: self.mover_jugador(1, 0))
        self.root.bind("<Left>", lambda e: self.mover_jugador(0, -1))
        self.root.bind("<Right>", lambda e: self.mover_jugador(0, 1))

    def dibujar_mapa(self):
        """Dibuja el mapa en el Canvas."""
        alto, ancho = len(self.mapa), len(self.mapa[0])
        for i in range(alto):
            for j in range(ancho):
                celda = tipo_de_celda(self.mapa[i][j])
                x1, y1 = j*self.cell_size, i*self.cell_size
                x2, y2 = x1+self.cell_size, y1+self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=celda.color(), outline="black")

    def mover_jugador(self, di, dj):
        """Mueve al jugador si la celda destino es válida."""
        if self.jugador.mover(di, dj, self.mapa, es_jugador=True):
            i, j = self.jugador.posicion()
            x1, y1 = j*self.cell_size+5, i*self.cell_size+5
            x2, y2 = x1+self.cell_size-10, y1+self.cell_size-10
            self.canvas.coords(self.jugador_sprite, x1, y1, x2, y2)