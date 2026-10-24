from src.hex_ai.board import HexBoard
from src.hex_ai.heuristics import evaluate_move_greedy, heuristica


def test_greedy_score():
    b = HexBoard(5)
    b.place(2, 2, 1)
    score = evaluate_move_greedy(b, (2, 3), 1)
    assert score > 0


def test_heuristica():
    b = HexBoard(5)
    b.place(0, 0, 1)
    h = heuristica(b, 1)
    assert isinstance(h, (int, float))