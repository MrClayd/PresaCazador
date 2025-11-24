import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from Main import iniciar

imagenes = ["Imagenes\\ESE_1_M.png", "Imagenes\\ESE_2_M.png", "Imagenes\\ESE_3_M.png",
            "Imagenes\\ESE_9_M.png", "Imagenes\\ESE_3_VA_M.png", "Imagenes\\ESE_6_M.png"]
indice_actual = 0

# --- Función para crear menú principal ---
def crear_menu():
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

    # --- NUEVO: ventana de dificultad ---
    def seleccionar_dificultad():
        ventana.withdraw()  # ocultar menú principal
        dif_win = tk.Toplevel()
        dif_win.title("Seleccionar Dificultad")
        dif_win.geometry("400x400")
        dif_win.resizable(False, False)

        tk.Label(dif_win, text="Elige la dificultad", font=("Arial", 18, "bold")).pack(pady=20)

        tk.Button(dif_win, text="Fácil", font=("Arial", 14),
                command=lambda: iniciar_juego(dif_win, ventana, "facil")).pack(pady=10)
        tk.Button(dif_win, text="Normal", font=("Arial", 14),
                command=lambda: iniciar_juego(dif_win, ventana, "normal")).pack(pady=10)
        tk.Button(dif_win, text="Difícil", font=("Arial", 14),
                command=lambda: iniciar_juego(dif_win, ventana, "dificil")).pack(pady=10)

        # Botón para volver al menú
        tk.Button(dif_win, text="Volver al menú",
            command=lambda: volver_menu(dif_win, ventana),
          **estilo_boton).pack(pady=20)
        
    def iniciar_juego(dif_win, ventana, dificultad):
        dif_win.destroy()   # cerrar ventana de dificultad
        ventana.destroy()   # cerrar menú principal
        iniciar(dificultad) # iniciar juego con dificultad

    def volver_menu(dif_win, ventana):
        dif_win.destroy()
        ventana.deiconify()  # volver a mostrar menú principal

    # --- Botones del menú principal ---
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

    tk.Button(ventana, text="Jugar", command=seleccionar_dificultad, **estilo_boton).place(x=810, y=250)
    tk.Button(ventana, text="Salir", command=ventana.destroy, **estilo_boton).place(x=810, y=600)
    tk.Button(ventana, text="Ver Puntajes",  **estilo_boton).place(x=600, y=350)
    tk.Button(ventana, text="Personalización de Personaje", **estilo_boton).place(x=1000, y=350)
    tk.Button(ventana, text="Sonido", **estilo_boton).place(x=600, y=500)
    tk.Button(ventana, text="Instrucciones", **estilo_boton).place(x=1000, y=500)

    ventana.mainloop()

# --- Ejecutar menú principal ---
crear_menu()