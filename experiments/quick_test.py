"""
Test rápido: mide cuánto tarda un enfrentamiento individual.
Sirve para calibrar los parámetros antes de correr el torneo completo.
"""
import time
from src.hex_ai.game import HexGame
from src.hex_ai.players.random_player import RandomPlayer
from src.hex_ai.players.greedy_player import GreedyPlayer
from src.hex_ai.players.minimax_player import MinimaxPlayer
from src.hex_ai.players.mcts_player import MCTSPlayer


def time_one_game(p1_class, p2_class, size, kwargs1, kwargs2):
    p1 = p1_class(1, **kwargs1)
    p2 = p2_class(2, **kwargs2)
    game = HexGame(p1, p2, size=size, verbose=False, allow_swap=False)
    t0 = time.time()
    winner = game.play()
    return time.time() - t0, winner, len(game.history)


if __name__ == "__main__":
    configs = [
        ("Random vs Random", RandomPlayer, RandomPlayer, {}, {}),
        ("Greedy vs Random", GreedyPlayer, RandomPlayer, {}, {}),
        ("Minimax_d2 vs Random", MinimaxPlayer, RandomPlayer,
            {"depth": 2, "time_limit": 1.5, "max_moves": 10}, {}),
        ("MCTS_01s vs Random", MCTSPlayer, RandomPlayer,
            {"time_limit": 0.1, "iterations": 200}, {}),
        ("Minimax_d2 vs MCTS_01s", MinimaxPlayer, MCTSPlayer,
            {"depth": 2, "time_limit": 1.5, "max_moves": 10},
            {"time_limit": 0.1, "iterations": 200}),
    ]

    for name, c1, c2, k1, k2 in configs:
        print(f"\n▶ {name} ...")
        t, w, moves = time_one_game(c1, c2, 7, k1, k2)
        print(f"   7x7: {t:.1f}s, {moves} turnos, ganador={w}")