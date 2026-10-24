from src.hex_ai.game import HexGame
from src.hex_ai.players.random_player import RandomPlayer


def test_game_runs():
    p1 = RandomPlayer(1)
    p2 = RandomPlayer(2)
    game = HexGame(p1, p2, size=5, verbose=False)
    winner = game.play()
    assert winner in (1, 2, None)