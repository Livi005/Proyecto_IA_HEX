"""
Jugador aleatorio. Sirve como baseline.
"""
import random
from .base import Player


class RandomPlayer(Player):
    def play(self, board):
        cells = board.empty_cells()
        if not cells:
            return None
        return random.choice(cells)