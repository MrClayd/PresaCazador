from collections import deque
from Mapa import CAMINO, LIANA, TUNEL
import heapq

def hay_camino_enemigo(mapa, inicio):
    """Verifica que un enemigo tenga al menos un camino accesible desde su posición."""
    alto, ancho = len(mapa), len(mapa[0])
    q = deque([inicio])
    visit = {inicio}
    while q:
        i, j = q.popleft()
        for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
            ni, nj = i+di, j+dj
            if 0 <= ni < alto and 0 <= nj < ancho:
                if mapa[ni][nj] in (CAMINO, LIANA) and (ni, nj) not in visit:
                    visit.add((ni, nj))
                    q.append((ni, nj))
    return len(visit) > 1  # si solo visitó su celda, está encerrado

def bfs(mapa, inicio, objetivo, es_jugador=False):
    alto, ancho = len(mapa), len(mapa[0])
    visitados = set()
    cola = deque([(inicio, [])])

    while cola:
        (i, j), camino = cola.popleft()
        if (i, j) == objetivo:
            return camino[0] if camino else (0, 0)

        if (i, j) in visitados:
            continue
        visitados.add((i, j))

        for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
            ni, nj = i+di, j+dj
            if 0 <= ni < alto and 0 <= nj < ancho:
                celda = mapa[ni][nj]
                if es_jugador and celda in (CAMINO, TUNEL):
                    cola.append(((ni, nj), camino+[(di, dj)]))
                elif not es_jugador and celda in (CAMINO, LIANA):
                    cola.append(((ni, nj), camino+[(di, dj)]))
    return (0, 0)


#prueba de esqueleto A*
def heuristica(a, b):
    """Distancia Manhattan como heurística."""
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(mapa, inicio, objetivo, es_jugador=False):
    alto, ancho = len(mapa), len(mapa[0])
    open_set = []
    heapq.heappush(open_set, (0, inicio, []))
    g_score = {inicio: 0}
    visitados = set()

    while open_set:
        _, (i, j), camino = heapq.heappop(open_set)

        if (i, j) == objetivo:
            return camino[0] if camino else (0, 0)

        if (i, j) in visitados:
            continue
        visitados.add((i, j))

        for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
            ni, nj = i+di, j+dj
            if 0 <= ni < alto and 0 <= nj < ancho:
                celda = mapa[ni][nj]
                valido = (es_jugador and celda in (CAMINO, TUNEL)) or (not es_jugador and celda in (CAMINO, LIANA))
                if valido:
                    nuevo_g = g_score[(i, j)] + 1
                    if (ni, nj) not in g_score or nuevo_g < g_score[(ni, nj)]:
                        g_score[(ni, nj)] = nuevo_g
                        f_score = nuevo_g + heuristica((ni, nj), objetivo)
                        heapq.heappush(open_set, (f_score, (ni, nj), camino+[(di, dj)]))

    return (0, 0)  # si no hay camino