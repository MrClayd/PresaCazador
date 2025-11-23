import tkinter as tk
from Mapa import generar_mapa
from Interfaz import Interfaz

def iniciar(dificultad="normal"):
    # Crear ventana principal del juego
    root = tk.Tk()
    root.title("Wild Bound")

    # Generar mapa
    mapa, inicio, salida = generar_mapa(16,16)

    # Crear interfaz con dificultad seleccionada
    app = Interfaz(root, mapa, inicio, salida, dificultad=dificultad)

    root.mainloop()