import tkinter as tk
from Mapa import generar_mapa
from Interfaz import Interfaz

def iniciar():
    root = tk.Tk()
    root.title("Mapa aleatorio 10x10")
    mapa = generar_mapa(10, 10)  # cada vez será distinto
    Interfaz(root, mapa)
    root.mainloop()

if __name__ == "__main__":
    iniciar()