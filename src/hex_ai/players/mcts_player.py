"""
Jugador Monte Carlo Tree Search (MCTS) para HEX con rollout heurístico.
"""
import math
import random
import time
from .base import Player
from ..heuristics import evaluate_move_greedy


class MCTSNode:
    def __init__(self, board, player_to_move, parent=None, move=None):
        self.board = board
        self.player_to_move = player_to_move
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = board.empty_cells()
        random.shuffle(self.untried_moves)

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def is_terminal(self):
        return self.board.is_winner(1) or self.board.is_winner(2) or self.board.is_full()

    def best_child(self, c_param=1.41):
        choices = [
            (child.wins / child.visits)
            + c_param * math.sqrt(math.log(self.visits) / child.visits)
            for child in self.children
        ]
        return self.children[choices.index(max(choices))]

    def expand(self):
        move = self.untried_moves.pop()
        new_board = self.board.clone()
        new_board.place(move[0], move[1], self.player_to_move)
        child = MCTSNode(new_board, 3 - self.player_to_move, parent=self, move=move)
        self.children.append(child)
        return child

    def rollout(self, root_player):
        """Simula una partida con política heurística (greedy) y algo de ruido."""
        board = self.board.clone()
        player = self.player_to_move

        while not board.is_full():
            if board.is_winner(1):
                return 1
            if board.is_winner(2):
                return 2

            cells = board.empty_cells()
            if not cells:
                break

            # Política: 80% greedy, 20% random (exploración)
            if random.random() < 0.8:
                move = max(cells, key=lambda m: evaluate_move_greedy(board, m, player))
            else:
                move = random.choice(cells)

            board.place(move[0], move[1], player)
            player = 3 - player

        return None

    def backpropagate(self, winner, root_player):
        self.visits += 1
        if winner == root_player:
            self.wins += 1
        elif winner is None:
            self.wins += 0.5  # empate cuenta como medio punto
        if self.parent:
            self.parent.backpropagate(winner, root_player)


class MCTSPlayer(Player):
    def __init__(self, player_id, time_limit=3.0, iterations=1000):
        super().__init__(player_id)
        self.time_limit = time_limit
        self.iterations = iterations

    def play(self, board):
        if board.is_full():
            return None

        root = MCTSNode(board.clone(), self.player_id)
        start = time.time()
        it = 0

        while time.time() - start < self.time_limit and it < self.iterations:
            node = root

            # 1. Selección
            while not node.is_terminal() and node.is_fully_expanded():
                node = node.best_child()

            # 2. Expansión
            if not node.is_terminal() and node.untried_moves:
                node = node.expand()

            # 3. Simulación
            winner = node.rollout(self.player_id)

            # 4. Retropropagación
            node.backpropagate(winner, self.player_id)
            it += 1

        if not root.children:
            cells = board.empty_cells()
            return cells[0] if cells else None

        # Elegir el hijo con más visitas (robusto)
        best = max(root.children, key=lambda c: c.visits)
        return best.move