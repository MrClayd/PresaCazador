import tkinter as tk
from Mapa import generar_mapa
from Interfaz import Interfaz

def iniciar():
    root = tk.Tk()
    root.title("Escapa del Cazador")
    mapa, inicio, salida = generar_mapa(16, 16)  
    Interfaz(root, mapa, inicio, salida)
    root.mainloop()

if __name__ == "__main__":
    iniciar()