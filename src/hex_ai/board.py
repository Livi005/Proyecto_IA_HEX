"""
Representación eficiente del tablero HEX usando NumPy.

Convención:
- 0 = celda vacía
- 1 = jugador 1 (conecta arriba-abajo, filas)
- 2 = jugador 2 (conecta izquierda-derecha, columnas)

El tablero es una matriz NxN donde el movimiento se hace por (fila, columna).
Los vecinos en HEX son 6: arriba, abajo, izquierda, derecha, y dos diagonales.
"""
import numpy as np


# Direcciones de los 6 vecinos en un tablero HEX "offset" (odd-r o even-r)
# Usamos offset tipo "odd-r" (fila impar desplazada a la derecha)
DIRECCIONES = [
    (-1, 0),   # arriba
    (-1, 1),   # arriba-derecha
    (0, -1),   # izquierda
    (0, 1),    # derecha
    (1, -1),   # abajo-izquierda
    (1, 0),    # abajo
]


class HexBoard:
    def __init__(self, size=11):
        self.size = size
        self.board = np.zeros((size, size), dtype=np.int8)
        self.last_move = None

    def clone(self):
        """Copia rápida sin deepcopy."""
        new = HexBoard(self.size)
        new.board = self.board.copy()
        new.last_move = self.last_move
        return new

    def is_valid(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size and self.board[row, col] == 0

    def place(self, row, col, player):
        if not self.is_valid(row, col):
            raise ValueError(f"Movimiento inválido: ({row}, {col})")
        self.board[row, col] = player
        self.last_move = (row, col)

    def empty_cells(self):
        """Devuelve lista de celdas vacías como tuplas (r, c)."""
        rows, cols = np.where(self.board == 0)
        return list(zip(rows.tolist(), cols.tolist()))

    def neighbors(self, row, col):
        """Devuelve vecinos válidos dentro del tablero."""
        result = []
        for dr, dc in DIRECCIONES:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                result.append((nr, nc))
        return result

    def is_winner(self, player):
        """
        Verifica si el jugador ha ganado usando BFS iterativo.
        - Jugador 1: conecta fila 0 con fila N-1.
        - Jugador 2: conecta columna 0 con columna N-1.
        """
        if player == 1:
            start_cells = [(0, c) for c in range(self.size) if self.board[0, c] == 1]
            target = lambda r, c: r == self.size - 1
        else:
            start_cells = [(r, 0) for r in range(self.size) if self.board[r, 0] == 2]
            target = lambda r, c: c == self.size - 1

        visited = np.zeros_like(self.board, dtype=bool)
        stack = list(start_cells)
        while stack:
            r, c = stack.pop()
            if visited[r, c]:
                continue
            visited[r, c] = True
            if target(r, c):
                return True
            for nr, nc in self.neighbors(r, c):
                if not visited[nr, nc] and self.board[nr, nc] == player:
                    stack.append((nr, nc))
        return False

    def is_full(self):
        return not np.any(self.board == 0)

    def __str__(self):
        """Representación ASCII del tablero."""
        lines = []
        for r in range(self.size):
            indent = " " * r
            row_str = " ".join(
                "." if self.board[r, c] == 0 else ("X" if self.board[r, c] == 1 else "O")
                for c in range(self.size)
            )
            lines.append(f"{indent}{row_str}")
        return "\n".join(lines)