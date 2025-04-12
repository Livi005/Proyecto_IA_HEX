import math
import time
import copy
from hexboard import HexBoard
from player_base import Player

class SmartHexPlayer(Player):
    def __init__(self, player_id):
        super().__init__(player_id)

    def play(self, board: HexBoard) -> tuple:
        tiempo_inicio = time.time()
        profundidad_Max = 2
        tiempo = 2
        cant_Jugadas = 10

        copia_tablero = board.board
        jugador = self.player_id

        jugada_puente = puente_roto(copia_tablero, jugador)
        if jugada_puente:
            return jugada_puente

        _, mejor_jugada = minimax(copia_tablero, profundidad_Max, True, -math.inf, math.inf, jugador, tiempo_inicio, tiempo, cant_Jugadas, profundidad_Max)
        return mejor_jugada

def minimax(tablero, profundidad, maximizar, alfa, beta, jugador, tiempo_inicio, tiempo, cant_Jugadas, profundidad_Max):
    if profundidad == 0 or hay_ganador(tablero) or time.time() - tiempo_inicio > tiempo:
        return heuristica(tablero, jugador), None

    lista_jugadas = jugadas_puntuadas(tablero, jugador)
    lista_jugadas = lista_jugadas[:cant_Jugadas]

    mejor_jugada = None

    if maximizar:
        mejor_valor = -math.inf
        for _, jugada in lista_jugadas:
            nuevo_tablero = copy.deepcopy(tablero)
            realizar_jugada(nuevo_tablero, jugada, jugador)
            valor, _ = minimax(nuevo_tablero, profundidad - 1, False, alfa, beta, jugador, tiempo_inicio, tiempo, cant_Jugadas, profundidad_Max)
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_jugada = jugada
            alfa = max(alfa, valor)
            if beta <= alfa:
                break
        return mejor_valor, mejor_jugada
    else:
        peor_valor = math.inf
        oponente = 3 - jugador
        for _, jugada in lista_jugadas:
            nuevo_tablero = copy.deepcopy(tablero)
            realizar_jugada(nuevo_tablero, jugada, oponente)
            valor, _ = minimax(nuevo_tablero, profundidad - 1, True, alfa, beta, jugador, tiempo_inicio, tiempo, cant_Jugadas, profundidad_Max)
            if valor < peor_valor:
                peor_valor = valor
                mejor_jugada = jugada
            beta = min(beta, valor)
            if beta <= alfa:
                break
        return peor_valor, mejor_jugada

def heuristica(tablero, jugador):
    ganador = hay_ganador(tablero)
    if ganador == jugador:
        return 10000
    elif ganador == 3 - jugador:
        return -10000
    else:
        return sum(p for p, _ in jugadas_puntuadas(tablero, jugador))

def jugadas_puntuadas(tablero, jugador):
    tamaño = len(tablero)
    oponente = 3 - jugador
    jugadas_puntuadas = []

    def hay_puente(p1, p2):
        i1, j1 = p1
        i2, j2 = p2
        return abs(i1 - i2) == 2 and abs(j1 - j2) == 1 or abs(i1 - i2) == 1 and abs(j1 - j2) == 2

    mis_fichas = [(i, j) for i in range(tamaño) for j in range(tamaño) if tablero[i][j] == jugador]
    fichas_oponente = [(i, j) for i in range(tamaño) for j in range(tamaño) if tablero[i][j] == oponente]

    pendientes = puentes_pendientes(tablero, jugador)
    riesgos = puentes_en_riesgo(tablero, jugador)

    for i in range(tamaño):
        for j in range(tamaño):
            if tablero[i][j] != 0:
                continue

            pos = (i, j)
            puntuacion = 0

            conecta_mias = any(hay_puente(pos, celda) for celda in mis_fichas)
            conecta_oponente = any(hay_puente(pos, celda) for celda in fichas_oponente)

            if conecta_mias and conecta_oponente:
                puntuacion += 30
            elif conecta_mias:
                puntuacion += 20
            elif conecta_oponente:
                puntuacion += 8

            conexiones = sum(1 for celda in fichas_oponente if hay_puente(pos, celda))
            if conexiones >= 2:
                puntuacion += 12

            if casilla_en_camino(tablero, pos, jugador, hay_puente):
                puntuacion += 25

            if pos in pendientes:
                puntuacion += 20

            if pos in riesgos:
                puntuacion += 40

            jugadas_puntuadas.append((puntuacion, pos))

    if not jugadas_puntuadas:
        return [(0, (i, j)) for i in range(tamaño) for j in range(tamaño) if tablero[i][j] == 0]

    return sorted(jugadas_puntuadas, reverse=True)

def puentes_pendientes(tablero, jugador):
    tamaño = len(tablero)
    pendientes = set()
    adyacentes = lambda i, j: [(i + di, j + dj) for (di, dj) in [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]
                                if 0 <= i + di < tamaño and 0 <= j + dj < tamaño]

    def hay_puente(p1, p2):
        i1, j1 = p1
        i2, j2 = p2
        return (abs(i1 - i2) == 2 and abs(j1 - j2) == 1) or (abs(i1 - i2) == 1 and abs(j1 - j2) == 2)

    fichas = [(i, j) for i in range(tamaño) for j in range(tamaño) if tablero[i][j] == jugador]
    for i in range(len(fichas)):
        for j in range(i + 1, len(fichas)):
            f1, f2 = fichas[i], fichas[j]
            if hay_puente(f1, f2):
                comunes = set(adyacentes(*f1)).intersection(adyacentes(*f2))
                for p in comunes:
                    if tablero[p[0]][p[1]] == 0:
                        pendientes.add(p)
    return pendientes

def puentes_en_riesgo(tablero, jugador):
    tamaño = len(tablero)
    oponente = 3 - jugador
    en_riesgo = set()
    adyacentes = lambda i, j: [(i + di, j + dj) for (di, dj) in [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]
                                if 0 <= i + di < tamaño and 0 <= j + dj < tamaño]

    def hay_puente(p1, p2):
        i1, j1 = p1
        i2, j2 = p2
        return (abs(i1 - i2) == 2 and abs(j1 - j2) == 1) or (abs(i1 - i2) == 1 and abs(j1 - j2) == 2)

    fichas = [(i, j) for i in range(tamaño) for j in range(tamaño) if tablero[i][j] == jugador]
    for i in range(len(fichas)):
        for j in range(i + 1, len(fichas)):
            f1, f2 = fichas[i], fichas[j]
            if hay_puente(f1, f2):
                intermedias = set(adyacentes(*f1)).intersection(adyacentes(*f2))
                libres = [p for p in intermedias if tablero[p[0]][p[1]] == 0]
                ocupadas = [p for p in intermedias if tablero[p[0]][p[1]] == oponente]
                if len(libres) == 1 and len(ocupadas) == 1:
                    en_riesgo.add(libres[0])
    return en_riesgo

def casilla_en_camino(tablero, pos, jugador, es_puente):
    tamaño = len(tablero)
    frontera = [pos]
    visitados = set()

    def borde_inicio(p):
        i, j = p
        return (jugador == 1 and i == 0) or (jugador == 2 and j == 0)

    def borde_final(p):
        i, j = p
        return (jugador == 1 and i == tamaño - 1) or (jugador == 2 and j == tamaño - 1)

    conectado_inicio = conectado_final = False
    while frontera:
        actual = frontera.pop()
        if actual in visitados:
            continue
        visitados.add(actual)
        if borde_inicio(actual): conectado_inicio = True
        if borde_final(actual): conectado_final = True
        if conectado_inicio and conectado_final:
            return True
        for i in range(tamaño):
            for j in range(tamaño):
                vecino = (i, j)
                if vecino not in visitados and (tablero[i][j] == jugador or vecino == pos):
                    if es_puente(actual, vecino):
                        frontera.append(vecino)
    return False

def hay_ganador(tablero):
    tamaño = len(tablero)

    def dfs(i, j, jugador, visitado):
        if (i, j) in visitado:
            return False
        visitado.add((i, j))
        if jugador == 1 and i == tamaño - 1:
            return True
        if jugador == 2 and j == tamaño - 1:
            return True
        for (di, dj) in [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < tamaño and 0 <= nj < tamaño and tablero[ni][nj] == jugador:
                if dfs(ni, nj, jugador, visitado):
                    return True
        return False

    for j in range(tamaño):
        if tablero[0][j] == 1 and dfs(0, j, 1, set()):
            return 1
    for i in range(tamaño):
        if tablero[i][0] == 2 and dfs(i, 0, 2, set()):
            return 2
    return None

def realizar_jugada(tablero, jugada, jugador):
    i, j = jugada
    tablero[i][j] = jugador
    return tablero

def puente_roto(tablero, jugador):
    tamaño = len(tablero)
    oponente = 3 - jugador
    adyacentes = lambda i, j: [(i + di, j + dj) for (di, dj) in [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]
                                if 0 <= i + di < tamaño and 0 <= j + dj < tamaño]

    mis_fichas = [(i, j) for i in range(tamaño) for j in range(tamaño) if tablero[i][j] == jugador]
    for (i1, j1) in mis_fichas:
        for (i2, j2) in mis_fichas:
            if (i1, j1) >= (i2, j2):
                continue
            if abs(i1 - i2) == 2 and abs(j1 - j2) == 1 or abs(i1 - i2) == 1 and abs(j1 - j2) == 2:
                puntos = list(set(adyacentes(i1, j1)).intersection(adyacentes(i2, j2)))
                if len(puntos) == 2:
                    inter1, inter2 = puntos
                    if tablero[inter1[0]][inter1[1]] == oponente and tablero[inter2[0]][inter2[1]] == 0:
                        return inter2
                    if tablero[inter2[0]][inter2[1]] == oponente and tablero[inter1[0]][inter1[1]] == 0:
                        return inter1
    return None
