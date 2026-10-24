from src.hex_ai.board import HexBoard
from src.hex_ai.players.random_player import RandomPlayer
from src.hex_ai.players.greedy_player import GreedyPlayer
from src.hex_ai.players.minimax_player import MinimaxPlayer
from src.hex_ai.players.mcts_player import MCTSPlayer


def test_all_players_return_valid_move():
    b = HexBoard(5)
    b.place(2, 2, 1)
    for P in [RandomPlayer, GreedyPlayer]:
        p = P(2)
        move = p.play(b)
        assert b.is_valid(*move)

    # Minimax con poca profundidad
    p = MinimaxPlayer(2, depth=1, time_limit=0.5)
    move = p.play(b)
    assert b.is_valid(*move)

    # MCTS con poco tiempo
    p = MCTSPlayer(2, time_limit=0.5, iterations=50)
    move = p.play(b)
    assert b.is_valid(*move)