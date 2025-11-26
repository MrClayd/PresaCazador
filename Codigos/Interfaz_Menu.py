import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from Main import iniciar
from tkinter import simpledialog

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

    # --- Selección de modo ---
    def seleccionar_modo():
        ventana.withdraw()
        modo_win = tk.Toplevel()
        modo_win.title("Seleccionar Modo")
        modo_win.geometry("400x300")
        modo_win.resizable(False, False)

        tk.Label(modo_win, text="Elige el modo de juego", font=("Arial", 18, "bold")).pack(pady=20)

        tk.Button(modo_win, text="🚪 Modo 1: Escapa", font=("Arial", 14),
                command=lambda: seleccionar_dificultad(modo_win, ventana, "escapa")).pack(pady=10)

        tk.Button(modo_win, text="🎯 Modo 2: Cazador", font=("Arial", 14),
                command=lambda: seleccionar_dificultad(modo_win, ventana, "cazador")).pack(pady=10)

    # --- Selección de dificultad con nombre ---
    def seleccionar_dificultad(modo_win, ventana, modo):
        modo_win.destroy()
        dif_win = tk.Toplevel()
        dif_win.title("Seleccionar Dificultad")
        dif_win.geometry("400x400")
        dif_win.resizable(False, False)

        tk.Label(dif_win, text="Elige la dificultad", font=("Arial", 18, "bold")).pack(pady=20)

        tk.Button(dif_win, text="Atrás", font=("Arial", 12),
            command=lambda: [dif_win.destroy(), seleccionar_modo()]).pack(pady=20)

        def iniciar_con_nombre(dificultad):
            dif_win.destroy()
            nombre = simpledialog.askstring("Nombre", "Ingresa tu nombre:")
            if nombre:
                iniciar_juego(dif_win, ventana, dificultad, nombre, modo)

        tk.Button(dif_win, text="Fácil", font=("Arial", 14),
                command=lambda: iniciar_con_nombre("facil")).pack(pady=10)
        tk.Button(dif_win, text="Normal", font=("Arial", 14),
                command=lambda: iniciar_con_nombre("normal")).pack(pady=10)
        tk.Button(dif_win, text="Difícil", font=("Arial", 14),
                command=lambda: iniciar_con_nombre("dificil")).pack(pady=10)

        tk.Button(dif_win, text="Volver al menú", font=("Arial", 12),
                command=lambda: volver_menu(dif_win, ventana)).pack(pady=20)

    def iniciar_juego(dif_win, ventana, dificultad, nombre, modo="escapa"):
        dif_win.destroy()
        ventana.destroy()
        import Main
        Main.iniciar(dificultad, nombre, modo)

    def volver_menu(dif_win, ventana):
        dif_win.destroy()
        ventana.deiconify()

    def ver_puntajes():
        archivo = "puntajes.txt"
        puntajes = {"modo_escapa": [], "modo_cazador": []}

        try:
            with open(archivo, "r") as f:
                for linea in f:
                    partes = linea.strip().split(":")
                    if len(partes) == 3:
                        modo_guardado, jugador, valor = partes
                        try:
                            puntajes[modo_guardado].append((jugador, int(valor)))
                        except ValueError:
                            print(f"⚠️ Puntaje inválido en línea: {linea.strip()}")
        except FileNotFoundError:
            messagebox.showinfo("🏆 Puntajes", "No hay puntajes guardados aún.")
            return

        ventana.destroy()
        win = tk.Tk()
        win.title("🏆 Mejores Puntajes")
        win.geometry("400x500")
        win.resizable(False, False)

        tk.Label(win, text="🏆 Mejores Puntajes", font=("Arial", 18, "bold")).pack(pady=10)

        # --- Modo Escapa ---
        tk.Label(win, text="🚪 Modo Escapa:", font=("Arial", 14, "bold")).pack(pady=5)
        if puntajes["modo_escapa"]:
            for i, (jugador, p) in enumerate(sorted(puntajes["modo_escapa"], key=lambda x: x[1], reverse=True)[:5], 1):
                tk.Label(win, text=f"{i}. {jugador} ⭐ {p}", font=("Arial", 12)).pack()
        else:
            tk.Label(win, text="Sin puntajes registrados", font=("Arial", 12)).pack()

        # --- Modo Cazador ---
        tk.Label(win, text="🎯 Modo Cazador:", font=("Arial", 14, "bold")).pack(pady=10)
        if puntajes["modo_cazador"]:
            for i, (jugador, p) in enumerate(sorted(puntajes["modo_cazador"], key=lambda x: x[1], reverse=True)[:5], 1):
                tk.Label(win, text=f"{i}. {jugador} ⭐ {p}", font=("Arial", 12)).pack()
        else:
            tk.Label(win, text="Sin puntajes registrados", font=("Arial", 12)).pack()

        tk.Button(win, text="Volver al menú", font=("Arial", 12),
                    command=lambda: [win.destroy(), crear_menu()]).pack(pady=10)

        win.mainloop()

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

    tk.Button(ventana, text="Jugar", command=seleccionar_modo, **estilo_boton).place(x=810, y=250)
    tk.Button(ventana, text="Salir", command=ventana.destroy, **estilo_boton).place(x=810, y=600)
    tk.Button(ventana, text="Ver Puntajes", command=ver_puntajes, **estilo_boton).place(x=600, y=350)
    tk.Button(ventana, text="Personalización de Personaje", **estilo_boton).place(x=1000, y=350)
    tk.Button(ventana, text="Sonido", **estilo_boton).place(x=600, y=500)
    tk.Button(ventana, text="Instrucciones", **estilo_boton).place(x=1000, y=500)

    ventana.mainloop()

crear_menu()
