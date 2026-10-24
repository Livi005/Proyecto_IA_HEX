"""
Clase base abstracta para todos los jugadores.
"""
from abc import ABC, abstractmethod


class Player(ABC):
    def __init__(self, player_id):
        self.player_id = player_id

    @abstractmethod
    def play(self, board):
        """
        Recibe un HexBoard y devuelve una tupla (row, col) con la jugada.
        """
        pass