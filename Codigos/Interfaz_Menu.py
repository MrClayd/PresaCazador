import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from Main import iniciar

imagenes = ["Imagenes\\ESE_1_M.png", "Imagenes\\ESE_2_M.png", "Imagenes\\ESE_3_M.png",
            "Imagenes\\ESE_9_M.png", "Imagenes\\ESE_3_VA_M.png", "Imagenes\\ESE_6_M.png"]
indice_actual = 0

ventana = tk.Tk()
ventana.title("Menú Principal")
ventana.geometry("1920x1080")
ventana.resizable(False, False)

fondo_label = tk.Label(ventana)
fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

def cargar_imagen(ruta):
    try:
        imagen = Image.open(ruta)
        imagen = imagen.resize((1920, 1080), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(imagen)
    except Exception as e:
        print(f"Error al cargar {ruta}: {e}")
        return None

def rotar_imagen():
    global indice_actual
    imagen = cargar_imagen(imagenes[indice_actual])
    if imagen:
        fondo_label.config(image=imagen)
        fondo_label.image = imagen
    indice_actual = (indice_actual + 1) % len(imagenes)
    ventana.after(10000, rotar_imagen)

rotar_imagen()

# --- NUEVO: ventana de selección de dificultad ---
def seleccionar_dificultad():
    # Crear ventana secundaria
    dif_win = tk.Toplevel(ventana)
    dif_win.title("Seleccionar Dificultad")
    dif_win.geometry("400x300")
    dif_win.resizable(False, False)

    tk.Label(dif_win, text="Elige la dificultad", font=("Arial", 18, "bold")).pack(pady=20)

    tk.Button(dif_win, text="Fácil", font=("Arial", 14),
            command=lambda: iniciar_juego(dif_win, "facil")).pack(pady=10)
    tk.Button(dif_win, text="Normal", font=("Arial", 14),
            command=lambda: iniciar_juego(dif_win, "normal")).pack(pady=10)
    tk.Button(dif_win, text="Difícil", font=("Arial", 14),
            command=lambda: iniciar_juego(dif_win, "dificil")).pack(pady=10)

def iniciar_juego(dif_win, dificultad):
    dif_win.destroy()   # cerrar ventana de dificultad
    ventana.destroy()   # cerrar menú principal
    iniciar(dificultad) # llamar al juego con dificultad

# --- Funciones de otros botones ---
def ver_puntajes():
    print("Mostrando puntajes...")

def personalizar_personaje():
    print("Abriendo personalización de personaje...")

def ajustes_sonido():
    print("Abriendo ajustes de sonido...")

def mostrar_instrucciones():
    instrucciones = (
        "Instrucciones del juego:\n"
        "- Usa las teclas de dirección para moverte.\n"
        "- Evita chocar contra las paredes o contra ti mismo.\n"
        "- ¡Diviértete!"
    )
    messagebox.showinfo("Instrucciones", instrucciones)

def salir():
    ventana.destroy()

# Estilo de los botones
estilo_boton = {
    "font": ("Arial", 14),
    "width": 25,
    "height": 2,
    "bg": "#3a3a3a",
    "fg": "white",
    "activebackground": "#5a5a5a",
    "bd": 0
}
Transparente = "#17298F"

titulo = tk.Label(ventana, text="Wild bound", font=("Arial", 72, "bold"), bg=Transparente, fg="#CE9B1C")
titulo.place(x=700, y=100)

# Botones principales
tk.Button(ventana, text="Jugar", command=seleccionar_dificultad, **estilo_boton).place(x=810, y=250)
tk.Button(ventana, text="Ver Puntajes", command=ver_puntajes, **estilo_boton).place(x=600, y=350)
tk.Button(ventana, text="Personalización de Personaje", command=personalizar_personaje, **estilo_boton).place(x=1000, y=350)
tk.Button(ventana, text="Sonido", command=ajustes_sonido, **estilo_boton).place(x=600, y=500)
tk.Button(ventana, text="Instrucciones", command=mostrar_instrucciones, **estilo_boton).place(x=1000, y=500)
tk.Button(ventana, text="Salir", command=salir, **estilo_boton).place(x=810, y=600)

ventana.mainloop()