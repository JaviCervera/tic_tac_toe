from flask import Flask, jsonify, request

from game.move import move
from game.movement import Movement
from game.tic_tac_toe_state import TicTacToeState

app = Flask(__name__)


@app.route("/move", methods=["POST"])
def move_action():
    data = request.get_json()
    state = TicTacToeState(
        board=data["board"],
        current_player=data["current_player"],
        winner=data["winner"],
    )
    movement = Movement(data["row"], data["col"])
    state = move(state, movement)
    if state is None:
        return jsonify({"error": "Invalid movement"}), 400
    return jsonify(
        {
            "board": state.board,
            "current_player": state.current_player,
            "winner": state.winner,
        }
    ), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
