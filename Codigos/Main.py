import tkinter as tk
from Mapa import generar_mapa, Camino, Muro
from Interfaz import Interfaz

def iniciar(dificultad, nombre, modo="escapa"):
    # Crear ventana principal del juego
    root = tk.Tk()
    root.title("Wild Bound")

    # Generar mapa
    mapa, inicio, salida = generar_mapa(16,16)
    

    # Crear interfaz con dificultad seleccionada
    app = Interfaz(root, mapa, inicio, salida, dificultad=dificultad, nombre=nombre, modo=modo)
    root.mainloop()
