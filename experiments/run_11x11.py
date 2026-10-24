"""
Experimento específico en tablero 11x11.
Solo enfrenta Minimax vs MCTS con pocas partidas por el coste computacional.
"""
import csv
import os
import time
from src.hex_ai.game import HexGame
from src.hex_ai.players.minimax_player import MinimaxPlayer
from src.hex_ai.players.mcts_player import MCTSPlayer


def play_match(p1_class, p2_class, size, games, kwargs1, kwargs2):
    stats = {"p1_wins": 0, "p2_wins": 0, "draws": 0, "times": [],
             "wins_first": 0, "wins_second": 0}
    for i in range(games):
        if i % 2 == 0:
            p1 = p1_class(1, **kwargs1)
            p2 = p2_class(2, **kwargs2)
            p1_is_class1 = True
        else:
            p1 = p2_class(1, **kwargs2)
            p2 = p1_class(2, **kwargs1)
            p1_is_class1 = False

        game = HexGame(p1, p2, size=size, verbose=False)
        start = time.time()
        winner = game.play()
        stats["times"].append(time.time() - start)

        if winner == 1:
            stats["wins_first"] += 1
            if p1_is_class1: stats["p1_wins"] += 1
            else: stats["p2_wins"] += 1
        elif winner == 2:
            stats["wins_second"] += 1
            if p1_is_class1: stats["p2_wins"] += 1
            else: stats["p1_wins"] += 1
        else:
            stats["draws"] += 1

    stats["avg_time"] = sum(stats["times"]) / len(stats["times"])
    return stats


if __name__ == "__main__":
    os.makedirs("experiments/results", exist_ok=True)

    configs = [
        ("Minimax_d2", MinimaxPlayer, {"depth": 2, "time_limit": 3.0, "max_moves": 10}),
        ("MCTS_05s", MCTSPlayer, {"time_limit": 0.5, "iterations": 500}),
    ]

    print("Experimento en 11x11: Minimax_d2 vs MCTS_05s")
    stats = play_match(
        configs[0][1], configs[1][1],
        size=11, games=4,
        kwargs1=configs[0][2], kwargs2=configs[1][2],
    )
    print(f"Resultado: Minimax {stats['p1_wins']} - {stats['p2_wins']} MCTS")
    print(f"Primer jugador: {stats['wins_first']}, Segundo: {stats['wins_second']}")
    print(f"Tiempo medio por partida: {stats['avg_time']:.1f}s")

    with open("experiments/results/tournament_11x11.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["player1", "player2", "p1_wins", "p2_wins",
                         "wins_first", "wins_second", "draws", "avg_time"])
        writer.writerow(["Minimax_d2", "MCTS_05s",
                         stats["p1_wins"], stats["p2_wins"],
                         stats["wins_first"], stats["wins_second"],
                         stats["draws"], stats["avg_time"]])

    print("✅ Guardado en experiments/results/tournament_11x11.csv")