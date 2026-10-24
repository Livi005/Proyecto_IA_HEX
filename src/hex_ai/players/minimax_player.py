"""
Jugador Minimax con poda alfa-beta y heurísticas de HEX.
"""
import math
import time
from .base import Player
from ..heuristics import heuristica, evaluate_move_greedy


class MinimaxPlayer(Player):
    def __init__(self, player_id, depth=3, time_limit=3.0, max_moves=15):
        super().__init__(player_id)
        self.depth = depth
        self.time_limit = time_limit
        self.max_moves = max_moves
        self._deadline = None
        self._best_so_far = None

    def play(self, board):
        self._deadline = time.time() + self.time_limit
        self._best_so_far = None
        _, best_move = self._minimax(
            board, self.depth, True, -math.inf, math.inf
        )
        # Fallback: si no se encontró nada, usar la mejor heurística
        if best_move is None:
            moves = board.empty_cells()
            if not moves:
                return None
            best_move = max(moves, key=lambda m: evaluate_move_greedy(board, m, self.player_id))
        return best_move

    def _timeout(self):
        return time.time() > self._deadline

    def _minimax(self, board, depth, maximizing, alpha, beta):
        if (
            depth == 0
            or board.is_winner(self.player_id)
            or board.is_winner(3 - self.player_id)
            or board.is_full()
            or self._timeout()
        ):
            return heuristica(board, self.player_id), None

        moves = self._order_moves(board, self.player_id)
        if not moves:
            return heuristica(board, self.player_id), None

        best_move = None
        if maximizing:
            value = -math.inf
            for move in moves:
                new_board = board.clone()
                new_board.place(move[0], move[1], self.player_id)
                score, _ = self._minimax(new_board, depth - 1, False, alpha, beta)
                if score > value:
                    value = score
                    best_move = move
                    self._best_so_far = move
                alpha = max(alpha, value)
                if beta <= alpha or self._timeout():
                    break
            return value, best_move
        else:
            value = math.inf
            opponent = 3 - self.player_id
            for move in moves:
                new_board = board.clone()
                new_board.place(move[0], move[1], opponent)
                score, _ = self._minimax(new_board, depth - 1, True, alpha, beta)
                if score < value:
                    value = score
                    best_move = move
                beta = min(beta, value)
                if beta <= alpha or self._timeout():
                    break
            return value, best_move

    def _order_moves(self, board, player):
        """Ordena movimientos por heurística simple para mejorar la poda."""
        moves = board.empty_cells()
        scored = [(evaluate_move_greedy(board, m, player), m) for m in moves]
        scored.sort(reverse=True, key=lambda x: x[0])
        return [m for _, m in scored[: self.max_moves]]