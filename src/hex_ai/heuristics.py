"""
Heurísticas específicas del dominio HEX.
"""
import numpy as np
from .utils import shared_neighbors, is_bridge


def evaluate_move_greedy(board, move, player):
    """
    Heurística simple: puntúa un movimiento según cuántas fichas propias
    y del oponente tiene cerca.
    """
    r, c = move
    score = 0
    for nr, nc in board.neighbors(r, c):
        val = board.board[nr, nc]
        if val == player:
            score += 2
        elif val == 3 - player:
            score += 1
    # Bonus por cercanía a los bordes objetivo
    size = board.size
    if player == 1:
        score += (size - abs(r - 0)) * 0.1
        score += (size - abs(r - (size - 1))) * 0.1
    else:
        score += (size - abs(c - 0)) * 0.1
        score += (size - abs(c - (size - 1))) * 0.1
    return score


def puentes_pendientes(board, player):
    """
    Devuelve el conjunto de celdas vacías que completarían un puente
    entre dos fichas propias.
    """
    size = board.size
    grid = board.board
    fichas = [(r, c) for r in range(size) for c in range(size) if grid[r, c] == player]
    pendientes = set()
    for i in range(len(fichas)):
        for j in range(i + 1, len(fichas)):
            f1, f2 = fichas[i], fichas[j]
            if is_bridge(f1, f2):
                comunes = shared_neighbors(f1, f2, size)
                for p in comunes:
                    if grid[p[0], p[1]] == 0:
                        pendientes.add(p)
    return pendientes


def puentes_en_riesgo(board, player):
    """
    Devuelve celdas vacías donde un puente propio tiene una sola salida
    y la otra está ocupada por el oponente.
    """
    size = board.size
    grid = board.board
    oponente = 3 - player
    fichas = [(r, c) for r in range(size) for c in range(size) if grid[r, c] == player]
    en_riesgo = set()
    for i in range(len(fichas)):
        for j in range(i + 1, len(fichas)):
            f1, f2 = fichas[i], fichas[j]
            if is_bridge(f1, f2):
                comunes = shared_neighbors(f1, f2, size)
                libres = [p for p in comunes if grid[p[0], p[1]] == 0]
                ocupadas = [p for p in comunes if grid[p[0], p[1]] == oponente]
                if len(libres) == 1 and len(ocupadas) == 1:
                    en_riesgo.add(libres[0])
    return en_riesgo


def heuristica(board, player):
    """
    Evaluación global del tablero desde la perspectiva del jugador.
    Suma puntuaciones de todas las celdas vacías.
    """
    if board.is_winner(player):
        return 100000
    if board.is_winner(3 - player):
        return -100000

    score = 0
    pendientes = puentes_pendientes(board, player)
    riesgos = puentes_en_riesgo(board, player)

    for move in board.empty_cells():
        r, c = move
        s = evaluate_move_greedy(board, move, player)
        if move in pendientes:
            s += 20
        if move in riesgos:
            s += 40
        score += s
    return score