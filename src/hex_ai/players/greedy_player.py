"""
Jugador greedy: elige la jugada que maximiza la heurística simple.
"""
from .base import Player
from ..heuristics import evaluate_move_greedy


class GreedyPlayer(Player):
    def play(self, board):
        cells = board.empty_cells()
        if not cells:
            return None
        best_score = -float("inf")
        best_move = cells[0]
        for move in cells:
            score = evaluate_move_greedy(board, move, self.player_id)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move