"""
Interfaz web con Flask para jugar HEX contra la IA.
"""
from flask import Flask, render_template, request, jsonify
from src.hex_ai.board import HexBoard
from src.hex_ai.players.mcts_player import MCTSPlayer

app = Flask(__name__, template_folder="templates", static_folder="static")

game_state = {
    "board": HexBoard(7),
    "human_player": 1,
    "ai_player": MCTSPlayer(2, time_limit=1.0, iterations=300),
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/state")
def state():
    b = game_state["board"]
    return jsonify({
        "board": b.board.tolist(),
        "size": b.size,
        "winner": 1 if b.is_winner(1) else (2 if b.is_winner(2) else None),
    })


@app.route("/move", methods=["POST"])
def move():
    data = request.get_json()
    r, c = data["row"], data["col"]
    b = game_state["board"]

    if not b.is_valid(r, c) or b.is_winner(1) or b.is_winner(2):
        return jsonify({"error": "Movimiento inválido"}), 400

    b.place(r, c, game_state["human_player"])
    if b.is_winner(game_state["human_player"]):
        return jsonify({"ok": True, "winner": 1})

    ai_move = game_state["ai_player"].play(b)
    if ai_move:
        b.place(ai_move[0], ai_move[1], game_state["ai_player"].player_id)

    winner = 2 if b.is_winner(2) else None
    return jsonify({"ok": True, "ai_move": ai_move, "winner": winner})


@app.route("/reset", methods=["POST"])
def reset():
    game_state["board"] = HexBoard(7)
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True)