from flask import Flask, jsonify, request

from game.tic_tac_toe import (
    InvalidMovementError,
    InvalidPositionError,
    Movement,
    TicTacToeState,
)
from game.move_impl import move_impl

app = Flask(__name__)


@app.route("/move", methods=["POST"])
def move():
    data = request.get_json()
    state = TicTacToeState(
        board=data["board"],
        current_player=data["current_player"],
        winner=data["winner"],
    )
    try:
        movement = Movement(data["row"], data["col"])
    except InvalidPositionError as exc:
        return jsonify({"error": str(exc)}), 400
    try:
        state = move_impl(state, movement)
        return jsonify(
            {
                "board": state.board,
                "current_player": state.current_player,
                "winner": state.winner,
            }
        ), 200
    except InvalidMovementError as exc:
        return jsonify({"error": str(exc)}), 400


if __name__ == "__main__":
    app.run(debug=True)
