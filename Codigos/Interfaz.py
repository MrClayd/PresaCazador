import tkinter as tk
import time
import random
from Mapa import Camino, Liana, Tunel, Muro, Salida
from Entidades import Jugador, Enemigo
from trampas import Trampa
from Energia import Energia
from pathfinding import bfs, astar
from tkinter import messagebox


class Interfaz:
    def __init__(self, root, mapa, inicio, salida, dificultad="normal", nombre="Jugador", modo="escapa"):
        self.root = root
        self.mapa = mapa
        self.cell_size = 40
        if isinstance(salida, Salida):
            self.salida = (salida.i, salida.j)
        else:
            self.salida = salida  # ya es tupla (i, j)
        self.tiempo_inicio = time.time()
        self.dificultad = dificultad
        self.nombre = nombre
        self.puntaje = 0
        self.modo = modo
        self.enemigos_atrapados = 0
        self.enemigos_escapados = 0 

        alto, ancho = len(mapa), len(mapa[0])
        self.canvas = tk.Canvas(root, width=ancho*self.cell_size, height=alto*self.cell_size)
        self.canvas.pack()

        self.dibujar_mapa()

        if dificultad == "facil":
            self.velocidad_enemigo = 1500
        elif dificultad == "normal":
            self.velocidad_enemigo = 1000
        elif dificultad == "dificil":
            self.velocidad_enemigo = 500

        # Jugador
        self.jugador = Jugador(*inicio)
        self.jugador_sprite = self.canvas.create_oval(
            inicio[1]*self.cell_size+5, inicio[0]*self.cell_size+5,
            inicio[1]*self.cell_size+self.cell_size-5, inicio[0]*self.cell_size+self.cell_size-5,
            fill="red", tags="jugador"
        )

        # Enemigos iniciales con roles
        self.enemigos = []
        posiciones_generadas = set()
        intentos = 0

        while len(posiciones_generadas) < 3 and intentos < 500:
            intentos += 1
            i = random.randrange(1, alto-1)
            j = random.randrange(1, ancho-1)
            if (i, j) != tuple(inicio) and (i, j) not in posiciones_generadas and (
                isinstance(self.mapa[i][j], Camino) or isinstance(self.mapa[i][j], Liana)
            ):
                posiciones_generadas.add((i, j))

        for (i, j) in posiciones_generadas:
            enemigo = Enemigo(i, j)
            if self.modo == "cazador":
                # en modo cazador todos los enemigos son cazadores
                enemigo.rol = "cazador"
            else:
                # en modo escapa asigna roles variados
                enemigo.rol = random.choice(["cazador", "emboscador", "erratico", "acechador", "patrullero"])

            sprite = self.canvas.create_rectangle(
                j*self.cell_size+5, i*self.cell_size+5,
                j*self.cell_size+self.cell_size-5, i*self.cell_size+self.cell_size-5,
                fill="yellow", tags="enemigo"
            )
            self.enemigos.append([enemigo, sprite])
            

        # Trampas
        self.trampas = []
        self.ultimo_colocada = 0

        # Energía
        self.energia = Energia(max_energia=10)
        self.ultimo_movimiento = 0
        self.cooldown = 0.5

        # Barra de energía
        self.energia_bar = tk.Canvas(root, width=200, height=20, bg="gray")
        self.energia_bar.pack(pady=5)
        self.actualizar_barra_energia()

        # HUD de roles de enemigos
        self.hud_roles = tk.Canvas(root, width=300, height=100, bg="lightgray")
        self.hud_roles.pack(pady=5)
        self.actualizar_hud_roles()


        # Bind de teclas
        self.root.bind("<Up>", lambda e: self.mover_jugador(-1, 0, correr=False))
        self.root.bind("<Down>", lambda e: self.mover_jugador(1, 0, correr=False))
        self.root.bind("<Left>", lambda e: self.mover_jugador(0, -1, correr=False))
        self.root.bind("<Right>", lambda e: self.mover_jugador(0, 1, correr=False))
        self.root.bind("<Shift-Up>", lambda e: self.mover_jugador(-1, 0, correr=True))
        self.root.bind("<Shift-Down>", lambda e: self.mover_jugador(1, 0, correr=True))
        self.root.bind("<Shift-Left>", lambda e: self.mover_jugador(0, -1, correr=True))
        self.root.bind("<Shift-Right>", lambda e: self.mover_jugador(0, 1, correr=True))
        self.root.bind("<space>", lambda e: self.colocar_trampa())

        self.mover_enemigo()

    def dibujar_mapa(self):
        alto, ancho = len(self.mapa), len(self.mapa[0])
        for i in range(alto):
            for j in range(ancho):
                celda = self.mapa[i][j]
                x1, y1 = j*self.cell_size, i*self.cell_size
                x2, y2 = x1+self.cell_size, y1+self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=celda.color(), outline="black")

    def actualizar_barra_energia(self):
        self.energia_bar.delete("all")
        porcentaje = self.energia.actual / self.energia.max_energia
        ancho = int(200 * porcentaje)
        color = "green" if porcentaje > 0.5 else "orange" if porcentaje > 0.2 else "red"
        self.energia_bar.create_rectangle(0, 0, ancho, 20, fill=color)

    def mover_jugador(self, di, dj, correr=False):
        ahora = time.time()
        if ahora - self.ultimo_movimiento < self.cooldown:
            return

        if correr:
            if not self.energia.consumir(2):
                print("Sin energía para correr")
                return
            di *= 2
            dj *= 2

        # --- Siempre obtener posición actual del jugador ---
        moved = self.jugador.mover(di, dj, self.mapa, es_jugador=True)
        i, j = self.jugador.posicion()   # ✅ siempre definido

        if moved:
            x1, y1 = j*self.cell_size+5, i*self.cell_size+5
            x2, y2 = x1+self.cell_size-10, y1+self.cell_size-10
            self.canvas.coords(self.jugador_sprite, x1, y1, x2, y2)

        if self.modo == "cazador":
            # Si el jugador entra en la celda de un enemigo
            for enemigo_data in list(self.enemigos):
                enemigo, sprite = enemigo_data
                if (i, j) == enemigo.posicion():
                    print("¡Jugador atrapó a un cazador!")
                    self.canvas.delete(sprite)
                    self.enemigos.remove(enemigo_data)
                    self.puntaje += 100
                    self.enemigos_atrapados += 1   # ✅ ahora sí cuenta
                    if self.enemigos_atrapados >= 3:   # condición de victoria
                        self.finalizar_partida_cazador(victoria=True)
                        return
                    self.respawn_enemigo()
                    self.actualizar_hud_roles()

            if (i, j) == self.salida:
                self.finalizar_partida()
                return

        self.ultimo_movimiento = ahora
        self.energia.regenerar()
        self.actualizar_barra_energia()


    def finalizar_partida(self):
        duracion = time.time() - self.tiempo_inicio
        base_puntaje = max(1000 - int(duracion), 0)

        if self.dificultad == "facil":
            factor = 1.0
        elif self.dificultad == "normal":
            factor = 1.5
        elif self.dificultad == "dificil":
            factor = 2.0

        puntaje_final = int(base_puntaje * factor) + self.puntaje

        self.root.after_cancel(self.mover_enemigo_id)
        self.guardar_puntaje("modo_escapa", self.nombre, puntaje_final)

        self.root.destroy()

        fin = tk.Tk()
        fin.title("🎉 Fin del Juego")
        fin.geometry("500x400")
        fin.resizable(False, False)

        tk.Label(fin, text="¡Has llegado a la salida!", font=("Arial", 20, "bold")).pack(pady=20)
        tk.Label(fin, text=f"⏱ Tiempo: {duracion:.2f} segundos", font=("Arial", 14)).pack(pady=10)
        tk.Label(fin, text=f"⭐ Puntaje: {puntaje_final}", font=("Arial", 14)).pack(pady=10)

        tk.Button(fin, text="Volver al menú", font=("Arial", 14),
                command=lambda: [fin.destroy(), __import__("Interfaz_Menu").crear_menu()]).pack(pady=20)
        tk.Button(fin, text="Salir", font=("Arial", 14), command=fin.destroy).pack(pady=10)

        fin.mainloop()

    def guardar_puntaje(self, modo, nombre, puntaje):
        archivo = "puntajes.txt"
        puntajes = {"modo_escapa": [], "modo_cazador": []}

        try:
            with open(archivo, "r") as f:
                for linea in f:
                    modo_guardado, jugador, valor = linea.strip().split(":")
                    puntajes[modo_guardado].append((jugador, int(valor)))
        except FileNotFoundError:
            pass

        puntajes[modo].append((nombre, puntaje))
        puntajes[modo] = sorted(puntajes[modo], key=lambda x: x[1], reverse=True)[:5]

        with open(archivo, "w") as f:
            for m in puntajes:
                for jugador, p in puntajes[m]:
                    f.write(f"{m}:{jugador}:{p}\n")

    def colocar_trampa(self):
        if self.modo == "cazador":
            return

        ahora = time.time()
        if len(self.trampas) < 3 and (ahora - self.ultimo_colocada) >= 5:
            i, j = self.jugador.posicion()
            if isinstance(self.mapa[i][j], Camino):  # ahora usamos la clase
                trampa = Trampa(i, j)
                self.trampas.append(trampa)
                self.ultimo_colocada = ahora
                trampa.id = self.canvas.create_rectangle(
                    j*self.cell_size+10, i*self.cell_size+10,
                    j*self.cell_size+self.cell_size-10, i*self.cell_size+self.cell_size-10,
                    fill="brown"
                )

    def mover_enemigo(self):
        if not self.enemigos:
            self.mover_enemigo_id = self.root.after(self.velocidad_enemigo, self.mover_enemigo)
            return

        posiciones_ocupadas = {enemigo.posicion() for enemigo, _ in self.enemigos}
        ji, jj = self.jugador.posicion()
        alto, ancho = len(self.mapa), len(self.mapa[0])

        for enemigo_data in list(self.enemigos):
            enemigo, sprite = enemigo_data
            ei, ej = enemigo.posicion()

            # --- Decisión según modo ---
            if self.modo == "cazador":
                objetivo = self.salida  # tupla (i, j)
                di, dj = astar(self.mapa, (ei, ej), objetivo, es_jugador=False)

                # Evitar al jugador si está cerca
                dist_jugador = abs(ei - ji) + abs(ej - jj)
                if dist_jugador <= 3:
                    # Elegir dirección ortogonal (no diagonal)
                    if abs(ei - ji) > abs(ej - jj):
                        # Priorizar eje vertical
                        if ji < ei: di, dj = 1, 0   # jugador arriba → enemigo baja
                        elif ji > ei: di, dj = -1, 0
                    else:
                        # Priorizar eje horizontal
                        if jj < ej: di, dj = 0, 1   # jugador izquierda → enemigo derecha
                        elif jj > ej: di, dj = 0, -1

                    # Fallback: si la celda elegida no es válida, elegir otra dirección aleatoria
                    nuevo_i, nuevo_j = ei + di, ej + dj
                    if not (0 <= nuevo_i < alto and 0 <= nuevo_j < ancho) or not self.mapa[nuevo_i][nuevo_j].permite_enemigo():
                        di, dj = random.choice([(-1,0),(1,0),(0,-1),(0,1)])

            else:
                # --- Decisión según rol (modo escapa) ---
                if enemigo.rol == "cazador":
                    di, dj = astar(self.mapa, (ei, ej), (ji, jj), es_jugador=False)
                elif enemigo.rol == "emboscador":
                    objetivo_i = ji + (ji - ei)
                    objetivo_j = jj + (jj - ej)
                    if not (0 <= objetivo_i < alto and 0 <= objetivo_j < ancho):
                        objetivo_i, objetivo_j = ji, jj
                    di, dj = bfs(self.mapa, (ei, ej), (objetivo_i, objetivo_j), es_jugador=False)
                elif enemigo.rol == "erratico":
                    if random.random() < 0.5:
                        di, dj = bfs(self.mapa, (ei, ej), (ji, jj), es_jugador=False)
                    else:
                        di, dj = random.choice([(-1,0),(1,0),(0,-1),(0,1)])
                elif enemigo.rol == "acechador":
                    dist = abs(ei - ji) + abs(ej - jj)
                    if dist < 6:
                        di, dj = bfs(self.mapa, (ei, ej), (ji, jj), es_jugador=False)
                    else:
                        di, dj = (0, 0)
                elif enemigo.rol == "patrullero":
                    di, dj = (0, 1) if random.random() < 0.5 else (0, -1)
                else:
                    di, dj = (0, 0)

            # --- Movimiento ---
            nuevo_i, nuevo_j = ei + di, ej + dj
            if not (0 <= nuevo_i < alto and 0 <= nuevo_j < ancho):
                continue
            if (nuevo_i, nuevo_j) in posiciones_ocupadas:
                continue

            posiciones_ocupadas.discard((ei, ej))
            if enemigo.mover(di, dj, self.mapa, es_jugador=False):
                posiciones_ocupadas.add((nuevo_i, nuevo_j))
                ei, ej = enemigo.posicion()
                x1, y1 = ej*self.cell_size+5, ei*self.cell_size+5
                x2, y2 = x1+self.cell_size-10, y1+self.cell_size-10
                self.canvas.coords(sprite, x1, y1, x2, y2)

                if self.modo == "cazador":
                    # Jugador atrapa enemigo
                    if (ei, ej) == (ji, jj):
                        print("¡Jugador atrapó a un cazador!")
                        self.canvas.delete(sprite)
                        self.enemigos.remove(enemigo_data)
                        self.puntaje += 100
                        self.enemigos_atrapados += 1
                        if self.enemigos_atrapados >= 3:  # condición de victoria
                            self.finalizar_partida_cazador(victoria=True)
                            return
                        self.respawn_enemigo()
                        self.actualizar_hud_roles()
                        continue

                    # Enemigo llega a salida
                    if (ei, ej) == self.salida:
                        print("¡Un cazador escapó!")
                        self.canvas.delete(sprite)
                        self.enemigos.remove(enemigo_data)
                        self.puntaje -= 50
                        self.enemigos_escapados += 1
                        if self.enemigos_escapados >= 5:  # condición de derrota
                            self.finalizar_partida_cazador(victoria=False)
                            return
                        self.respawn_enemigo()
                        self.actualizar_hud_roles()
                        continue

                else:
                    # --- Colisión con jugador (modo escapa) ---
                    if (ei, ej) == (ji, jj):
                        print("¡El enemigo atrapó al jugador!")
                        self.finalizar_derrota()
                        return
                    # --- Trampas ---
                    for trampa in list(self.trampas):
                        if (ei, ej) == trampa.posicion():
                            print("¡Enemigo atrapado por trampa!")
                            self.canvas.delete(trampa.id)
                            self.trampas.remove(trampa)
                            self.mapa[ei][ej] = Camino(ei, ej)
                            self.canvas.delete(sprite)
                            self.enemigos.remove(enemigo_data)
                            self.puntaje += 50
                            self.root.after(10000, self.respawn_enemigo)
                            self.actualizar_hud_roles()
                            break

        self.mover_enemigo_id = self.root.after(self.velocidad_enemigo, self.mover_enemigo)

    def respawn_enemigo(self):
        if len(self.enemigos) >= 3:
            return  # máximo 3 enemigos

        alto, ancho = len(self.mapa), len(self.mapa[0])
        ji, jj = self.jugador.posicion()

        for _ in range(300):
            i = random.randrange(1, alto-1)
            j = random.randrange(1, ancho-1)
            if (i, j) == (ji, jj):
                continue
            if any((i, j) == e.posicion() for e, _ in self.enemigos):
                continue
            if isinstance(self.mapa[i][j], Camino) or isinstance(self.mapa[i][j], Liana):
                enemigo = Enemigo(i, j)

                if self.modo == "cazador":
                    enemigo.rol = "cazador"
                else:
                    enemigo.rol = random.choice(["cazador", "emboscador", "erratico", "acechador", "patrullero"])

                sprite = self.canvas.create_rectangle(
                    j*self.cell_size+5, i*self.cell_size+5,
                    j*self.cell_size+self.cell_size-5, i*self.cell_size+self.cell_size-5,
                    fill="yellow", tags="enemigo"
                )
                self.enemigos.append([enemigo, sprite])
                self.actualizar_hud_roles()
                return

    def finalizar_derrota(self):
    # Puntaje cero en derrota
        puntaje_final = 0

        # Cancelar movimiento de enemigos
        self.root.after_cancel(self.mover_enemigo_id)
        self.guardar_puntaje("modo_escapa", self.nombre, puntaje_final)

        # Cerrar ventana de juego
        self.root.destroy()

        # Crear ventana de fin de juego (derrota)
        fin = tk.Tk()
        fin.title("💀 Fin del Juego")
        fin.geometry("500x400")
        fin.resizable(False, False)

        tk.Label(fin, text="Has sido atrapado 😢", font=("Arial", 20, "bold")).pack(pady=20)
        tk.Label(fin, text="Tu puntaje es 0", font=("Arial", 14)).pack(pady=10)

        tk.Button(fin, text="Volver al menú", font=("Arial", 14),
                command=lambda: [fin.destroy(), __import__("Interfaz_Menu").crear_menu()]).pack(pady=20)
        tk.Button(fin, text="Salir", font=("Arial", 14), command=fin.destroy).pack(pady=10)

        fin.mainloop()


    def actualizar_hud_roles(self):
        self.hud_roles.delete("all")
        x, y = 10, 10
        colores = {
            "cazador": "red",
            "emboscador": "blue",
            "erratico": "purple",
            "acechador": "orange",
            "patrullero": "green"
        }
        for idx, (enemigo, _) in enumerate(self.enemigos, start=1):
            rol = enemigo.rol
            color = colores.get(rol, "black")
            texto = f"Enemigo {idx}: {rol}"
            # Texto con color según rol
            self.hud_roles.create_text(x, y, anchor="nw", text=texto, font=("Arial", 12), fill=color)
            y += 20

    def finalizar_partida_cazador(self, victoria=True):
        self.root.after_cancel(self.mover_enemigo_id)
        modo = "modo_cazador"
        puntaje_final = self.puntaje

        self.guardar_puntaje(modo, self.nombre, puntaje_final)
        self.root.destroy()

        fin = tk.Tk()
        fin.title("🏆 Fin del Modo Cazador")
        fin.geometry("500x400")
        fin.resizable(False, False)

        if victoria:
            tk.Label(fin, text="¡Has atrapado suficientes cazadores!", font=("Arial", 20, "bold")).pack(pady=20)
        else:
            tk.Label(fin, text="Demasiados cazadores escaparon 😢", font=("Arial", 20, "bold")).pack(pady=20)

        tk.Label(fin, text=f"⭐ Puntaje: {puntaje_final}", font=("Arial", 14)).pack(pady=10)

        tk.Button(fin, text="Volver al menú", font=("Arial", 14),
                command=lambda: [fin.destroy(), __import__("Interfaz_Menu").crear_menu()]).pack(pady=20)
        tk.Button(fin, text="Salir", font=("Arial", 14), command=fin.destroy).pack(pady=10)

        fin.mainloop()