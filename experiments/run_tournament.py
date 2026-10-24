"""
Torneo round-robin entre jugadores de HEX.
Registra quién empieza cada partida y mide la ventaja del primer jugador.
"""
import csv
import os
from tqdm import tqdm
from src.hex_ai.game import HexGame
from src.hex_ai.players.random_player import RandomPlayer
from src.hex_ai.players.greedy_player import GreedyPlayer
from src.hex_ai.players.minimax_player import MinimaxPlayer
from src.hex_ai.players.mcts_player import MCTSPlayer


PLAYERS = {
    "Random":     (RandomPlayer, {}),
    "Greedy":     (GreedyPlayer, {}),
    "Minimax_d2": (MinimaxPlayer, {"depth": 2, "time_limit": 1.0, "max_moves": 10}),
    "MCTS_05s":   (MCTSPlayer,    {"time_limit": 0.5, "iterations": 200}),
}

BOARD_SIZE = 7
GAMES = 20


def play_match(player1_class, player2_class, size, games, kwargs1, kwargs2):
    stats = {
        "wins_first": 0, "wins_second": 0, "draws": 0,
        "times": [],
        "player1_class_wins": 0, "player2_class_wins": 0,
    }

    for i in range(games):
        if i % 2 == 0:
            p1 = player1_class(1, **kwargs1)
            p2 = player2_class(2, **kwargs2)
            p1_is_class1 = True
        else:
            p1 = player2_class(1, **kwargs2)
            p2 = player1_class(2, **kwargs1)
            p1_is_class1 = False

        game = HexGame(p1, p2, size=size, verbose=False, allow_swap=False)
        import time
        start = time.time()
        winner = game.play()
        stats["times"].append(time.time() - start)

        if winner == 1:
            stats["wins_first"] += 1
            if p1_is_class1:
                stats["player1_class_wins"] += 1
            else:
                stats["player2_class_wins"] += 1
        elif winner == 2:
            stats["wins_second"] += 1
            if p1_is_class1:
                stats["player2_class_wins"] += 1
            else:
                stats["player1_class_wins"] += 1
        else:
            stats["draws"] += 1

    stats["avg_time"] = sum(stats["times"]) / len(stats["times"])
    return stats


def main():
    os.makedirs("experiments/results", exist_ok=True)
    results = []
    names = list(PLAYERS.keys())

    # Contamos cuántos enfrentamientos únicos hay
    enfrentamientos = [(n1, n2) for i, n1 in enumerate(names) for n2 in names[i+1:]]

    print(f"Torneo en tablero {BOARD_SIZE}x{BOARD_SIZE}, {GAMES} partidas por enfrentamiento")
    print(f"Total enfrentamientos: {len(enfrentamientos)}\n")

    with tqdm(total=len(enfrentamientos), desc="Enfrentamientos") as pbar:
        for n1, n2 in enfrentamientos:
            p1_class, kwargs1 = PLAYERS[n1]
            p2_class, kwargs2 = PLAYERS[n2]

            pbar.set_postfix_str(f"{n1} vs {n2}")
            stats = play_match(
                p1_class, p2_class,
                size=BOARD_SIZE, games=GAMES,
                kwargs1=kwargs1, kwargs2=kwargs2,
            )

            results.append({
                "player1": n1, "player2": n2,
                "p1_class_wins": stats["player1_class_wins"],
                "p2_class_wins": stats["player2_class_wins"],
                "wins_first": stats["wins_first"],
                "wins_second": stats["wins_second"],
                "draws": stats["draws"],
                "avg_time": stats["avg_time"],
            })
            pbar.update(1)

    with open("experiments/results/tournament.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print("\n✅ Resultados guardados en experiments/results/tournament.csv")


if __name__ == "__main__":
    main()