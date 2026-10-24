"""
Lógica del juego HEX: turnos, validación, condición de victoria.
Incluye la regla opcional del "swap" (pie rule) para equilibrar la ventaja
estructural del primer jugador.
"""
from .board import HexBoard


class HexGame:
    def __init__(self, player1, player2, size=11, verbose=True, allow_swap=False):
        self.board = HexBoard(size)
        self.players = {1: player1, 2: player2}
        self.current = 1
        self.verbose = verbose
        self.allow_swap = allow_swap
        self.history = []
        self.swap_used = False
        self.winner = None

    def switch_turn(self):
        self.current = 3 - self.current

    def play(self):
        """Ejecuta una partida completa. Devuelve el ganador (1, 2 o None)."""
        while not self.board.is_full():
            player = self.players[self.current]
            move = player.play(self.board)
            if move is None:
                break
            r, c = move
            self.board.place(r, c, self.current)
            self.history.append((self.current, move))

            if self.verbose:
                print(f"\nTurno {len(self.history)} - Jugador {self.current} juega ({r}, {c})")
                print(self.board)

            if self.board.is_winner(self.current):
                self.winner = self.current
                if self.verbose:
                    print(f"\n🏆 ¡Ganó el jugador {self.current}!")
                return self.current

            # Regla del swap: solo tras la primera jugada del jugador 1
            if self.allow_swap and len(self.history) == 1 and not self.swap_used:
                if hasattr(self.players[2], "wants_swap") and self.players[2].wants_swap(self.board):
                    # Intercambiamos roles: el jugador 2 toma el color 1
                    self.players[1], self.players[2] = self.players[2], self.players[1]
                    self.players[1].player_id = 1
                    self.players[2].player_id = 2
                    self.swap_used = True
                    if self.verbose:
                        print("🔄 ¡El jugador 2 ha hecho swap!")

            self.switch_turn()

        if self.verbose:
            print("\nEmpate: tablero lleno.")
        return None


def main():
    """Partida de ejemplo: Minimax vs Random."""
    from .players.minimax_player import MinimaxPlayer
    from .players.random_player import RandomPlayer

    p1 = MinimaxPlayer(player_id=1, depth=3, time_limit=3.0)
    p2 = RandomPlayer(player_id=2)
    game = HexGame(p1, p2, size=7, verbose=True, allow_swap=False)
    game.play()


if __name__ == "__main__":
    main()