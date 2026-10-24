"""
Funciones para enfrentar jugadores y medir rendimiento.
"""
import time
from .game import HexGame


def play_match(player1_class, player2_class, size=7, games=10,
               kwargs1=None, kwargs2=None):
    """
    Enfrenta dos clases de jugador N veces (alternando quién empieza).
    kwargs1: dict con argumentos para player1_class
    kwargs2: dict con argumentos para player2_class
    """
    kwargs1 = kwargs1 or {}
    kwargs2 = kwargs2 or {}

    wins = {1: 0, 2: 0, "draw": 0}
    times = []

    for i in range(games):
        # Alternamos quién juega como jugador 1 y quién como 2
        if i % 2 == 0:
            p1 = player1_class(1, **kwargs1)
            p2 = player2_class(2, **kwargs2)
        else:
            p1 = player2_class(1, **kwargs2)
            p2 = player1_class(2, **kwargs1)

        game = HexGame(p1, p2, size=size, verbose=False)
        start = time.time()
        winner = game.play()
        times.append(time.time() - start)

        if winner is None:
            wins["draw"] += 1
        else:
            wins[winner] += 1

    return {
        "wins_p1": wins[1],
        "wins_p2": wins[2],
        "draws": wins["draw"],
        "avg_time": sum(times) / len(times),
    }