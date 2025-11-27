import tkinter as tk
from Audio_manager import AudioManager
from tkinter import messagebox
from PIL import Image, ImageTk
from Main import iniciar
from tkinter import simpledialog
import pygame

pygame.mixer.init()

imagenes = ["Imagenes\\ESE_1_M.png", "Imagenes\\ESE_2_M.png", "Imagenes\\ESE_3_M.png",
            "Imagenes\\ESE_9_M.png", "Imagenes\\ESE_3_VA_M.png", "Imagenes\\ESE_6_M.png"]
indice_actual = 0
audio = AudioManager()


def crear_menu():
    ventana = tk.Tk()
    ventana.title("Menú Principal")
    ventana.geometry("1920x1080")
    ventana.resizable(False, False)

    # Música del menú solo una vez
    audio.play_menu_music()

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

    
    # SUBVENTANAS
    #ventana modo de juego
    def seleccionar_modo():
        ventana.withdraw()
        modo_win = tk.Toplevel()
        modo_win.title("Seleccionar Modo")
        modo_win.geometry("400x300")

        tk.Label(modo_win, text="Elige el modo de juego", font=("Arial", 18, "bold")).pack(pady=20)

        tk.Button(modo_win, text="🚪 Modo 1: Escapa", font=("Arial", 14),
                command=lambda: seleccionar_dificultad(modo_win, "escapa")).pack(pady=10)

        tk.Button(modo_win, text="🎯 Modo 2: Cazador", font=("Arial", 14),
                command=lambda: seleccionar_dificultad(modo_win, "cazador")).pack(pady=10)

    #ventana dificultad
    def seleccionar_dificultad(modo_win, modo):
        modo_win.destroy()
        dif_win = tk.Toplevel()
        dif_win.title("Seleccionar Dificultad")
        dif_win.geometry("400x400")

        tk.Label(dif_win, text="Elige la dificultad", font=("Arial", 18, "bold")).pack(pady=20)

        tk.Button(dif_win, text="Atrás", font=("Arial", 12),
                command=lambda: [dif_win.destroy(), seleccionar_modo()]).pack(pady=20)

        #ventana de ingreso de nombre
        def iniciar_con_nombre(dificultad):
            dif_win.destroy()
            nombre_win = tk.Toplevel()
            nombre_win.title("Ingresar nombre")
            nombre_win.geometry("400x200")

            tk.Label(nombre_win, text="Ingresa tu nombre:", font=("Arial", 14)).pack(pady=10)
            entry_nombre = tk.Entry(nombre_win, font=("Arial", 12))
            entry_nombre.pack(pady=10)

            def confirmar_nombre():
                nombre = entry_nombre.get()
                if nombre:
                    nombre_win.destroy()

                    # Cambia a música del juego
                    audio.play_game_music()

                    
                    ventana.destroy()
                    iniciar(dificultad, nombre, modo)

            tk.Button(nombre_win, text="OK", font=("Arial", 12),
                    command=confirmar_nombre).pack(pady=5)

        tk.Button(dif_win, text="Fácil", font=("Arial", 14),
                command=lambda: iniciar_con_nombre("facil")).pack(pady=10)

        tk.Button(dif_win, text="Normal", font=("Arial", 14),
                command=lambda: iniciar_con_nombre("normal")).pack(pady=10)

        tk.Button(dif_win, text="Difícil", font=("Arial", 14),
                command=lambda: iniciar_con_nombre("dificil")).pack(pady=10)

    #Puntajes de los 2 modos
    def ver_puntajes():
        archivo = "puntajes.txt"
        puntajes = {"modo_escapa": [], "modo_cazador": []}

        try:
            with open(archivo, "r") as f:
                for linea in f:
                    partes = linea.strip().split(":")
                    if len(partes) == 3:
                        modo_guardado, jugador, valor = partes
                        puntajes[modo_guardado].append((jugador, int(valor)))
        except:
            messagebox.showinfo("🏆 Puntajes", "No hay puntajes guardados aún.")
            return

        ventana.withdraw()
        win = tk.Toplevel()
        win.title("🏆 Mejores Puntajes")
        win.geometry("400x500")

        tk.Label(win, text="🏆 Mejores Puntajes", font=("Arial", 18, "bold")).pack(pady=10)

        tk.Label(win, text="🚪 Modo Escapa:", font=("Arial", 14, "bold")).pack(pady=5)
        for i, (jugador, p) in enumerate(sorted(puntajes["modo_escapa"], key=lambda x: x[1], reverse=True)[:5], 1):
            tk.Label(win, text=f"{i}. {jugador} ⭐ {p}", font=("Arial", 12)).pack()

        tk.Label(win, text="🎯 Modo Cazador:", font=("Arial", 14, "bold")).pack(pady=10)
        for i, (jugador, p) in enumerate(sorted(puntajes["modo_cazador"], key=lambda x: x[1], reverse=True)[:5], 1):
            tk.Label(win, text=f"{i}. {jugador} ⭐ {p}", font=("Arial", 12)).pack()

        tk.Button(win, text="Volver al menú", font=("Arial", 12),
                command=lambda: [win.destroy(), ventana.deiconify()]).pack(pady=10)


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

    titulo = tk.Label(ventana, text="Wild bound", font=("Arial", 72, "bold"),
                    bg=Transparente, fg="#CE9B1C")
    titulo.place(x=700, y=100)

    tk.Button(ventana, text="Jugar", command=seleccionar_modo, **estilo_boton).place(x=810, y=250)
    tk.Button(ventana, text="Salir", command=ventana.destroy, **estilo_boton).place(x=810, y=500)
    tk.Button(ventana, text="Ver Puntajes", command=ver_puntajes, **estilo_boton).place(x=810, y=350)

    ventana.mainloop()


crear_menu()
