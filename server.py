from flask import Flask, jsonify, request

from game import TicTacToe, TicTacToeImpl

app = Flask(__name__)
game: TicTacToe = TicTacToeImpl()


@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    row, col = data['row'], data['col']
    success = game.make_move(row, col)
    if success:
        return jsonify({'board': game.get_board(), 'winner': game.check_winner()}), 200
    return jsonify({'error': 'Invalid move'}), 400


@app.route('/board', methods=['GET'])
def board():
    return jsonify({'board': game.get_board(), 'winner': game.check_winner()}), 200


@app.route('/reset', methods=['POST'])
def reset():
    game.reset_game()
    return jsonify({'board': game.get_board(), 'winner': game.check_winner()}), 200


if __name__ == '__main__':
    app.run(debug=True)
