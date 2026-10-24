"""
Diagnóstico del motor del juego HEX.
"""
from src.hex_ai.board import HexBoard
from src.hex_ai.game import HexGame
from src.hex_ai.players.random_player import RandomPlayer
from src.hex_ai.players.minimax_player import MinimaxPlayer


print("=" * 60)
print("TEST 1: Verificar is_winner en un tablero manual")
print("=" * 60)
b = HexBoard(5)
# Jugador 1 conecta columna 0 completa (debería ganar)
for r in range(5):
    b.place(r, 0, 1)
print(b)
print(f"¿Gana jugador 1? {b.is_winner(1)}  (esperado: True)")
print(f"¿Gana jugador 2? {b.is_winner(2)}  (esperado: False)")

print("\n" + "=" * 60)
print("TEST 2: Verificar clone()")
print("=" * 60)
b2 = HexBoard(5)
b2.place(0, 0, 1)
b3 = b2.clone()
b3.place(1, 1, 2)
print(f"Original en (1,1): {b2.board[1, 1]}  (esperado: 0)")
print(f"Clone en (1,1):    {b3.board[1, 1]}  (esperado: 2)")
print(f"¿Son arrays independientes? {b2.board is not b3.board}  (esperado: True)")

print("\n" + "=" * 60)
print("TEST 3: Partida Random vs Random — ¿quién gana?")
print("=" * 60)
wins = {1: 0, 2: 0, None: 0}
for i in range(20):
    p1 = RandomPlayer(1)
    p2 = RandomPlayer(2)
    game = HexGame(p1, p2, size=5, verbose=False)
    winner = game.play()
    wins[winner] += 1
print(f"Random vs Random: {wins}")
print("Esperado: ~50/50 si el motor es correcto")

print("\n" + "=" * 60)
print("TEST 4: Minimax vs Random — ¿gana Minimax?")
print("=" * 60)
wins = {1: 0, 2: 0, None: 0}
for i in range(10):
    p1 = MinimaxPlayer(1, depth=2, time_limit=2.0)
    p2 = RandomPlayer(2)
    game = HexGame(p1, p2, size=5, verbose=False)
    winner = game.play()
    wins[winner] += 1
print(f"Minimax(p1) vs Random(p2): {wins}")
print("Esperado: Minimax gana casi siempre")

print("\n" + "=" * 60)
print("TEST 5: Random(p1) vs Minimax(p2) — ¿gana Minimax?")
print("=" * 60)
wins = {1: 0, 2: 0, None: 0}
for i in range(10):
    p1 = RandomPlayer(1)
    p2 = MinimaxPlayer(2, depth=2, time_limit=2.0)
    game = HexGame(p1, p2, size=5, verbose=False)
    winner = game.play()
    wins[winner] += 1
print(f"Random(p1) vs Minimax(p2): {wins}")
print("Esperado: Minimax gana casi siempre")