import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Lista de imágenes subidas (ajusta los nombres si los cambias)
imagenes = ["ESE_1_M.png", "ESE_2_M.png", "ESE_3_M.png"]  # Usa los nombres reales de tus archivos
indice_actual = 0

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Menú Principal")
ventana.geometry("1920x1080")
ventana.resizable(False, False)

# Fondo con imagen
fondo_label = tk.Label(ventana)
fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

# Función para cargar y redimensionar imagen
def cargar_imagen(ruta):
    try:
        imagen = Image.open(ruta)
        imagen = imagen.resize((1920, 1080), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(imagen)
    except Exception as e:
        print(f"Error al cargar {ruta}: {e}")
        return None

# Función para rotar imágenes cada 5 segundos
def rotar_imagen():
    global indice_actual
    imagen = cargar_imagen(imagenes[indice_actual])
    if imagen:
        fondo_label.config(image=imagen)
        fondo_label.image = imagen
    indice_actual = (indice_actual + 1) % len(imagenes)
    ventana.after(5000, rotar_imagen)

# Iniciar rotación
rotar_imagen()

# Funciones de los botones
def jugar():
    print("Iniciando el juego...")

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
# Título
titulo = tk.Label(ventana, text="Wild bound", font=("Arial", 72, "bold"),bg=Transparente , fg="#CE9B1C")
titulo.place(x=700, y=100)
#ventana.wm_attributes('-transparentcolor', Transparente)
# Botones
tk.Button(ventana, text="Jugar", command=jugar, **estilo_boton).place(x=810, y=250)
tk.Button(ventana, text="Ver Puntajes", command=ver_puntajes, **estilo_boton).place(x=600, y=350)
tk.Button(ventana, text="Personalización de Personaje", command=personalizar_personaje, **estilo_boton).place(x=1000, y=350)
tk.Button(ventana, text="Sonido", command=ajustes_sonido, **estilo_boton).place(x=600, y=500)
tk.Button(ventana, text="Instrucciones", command=mostrar_instrucciones, **estilo_boton).place(x=1000, y=500)
tk.Button(ventana, text="Salir", command=salir, **estilo_boton).place(x=810, y=600)

ventana.mainloop()