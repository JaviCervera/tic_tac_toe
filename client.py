from game import Board, TicTacToe, TicTacToeProxy


def print_board(board: Board) -> None:
    for row in board:
        print(' | '.join(['X' if cell == 1 else 'O' if cell == 2 else ' ' for cell in row]))
        print('-' * 9)


def main() -> None:
    game: TicTacToe = TicTacToeProxy('http://127.0.0.1:5000')
    while True:
        action = input('Choose action: [move, reset, exit]: ').strip().lower()
        if action == 'reset':
            if game.reset_game():
                print('Game reset!')
                print_board(game.get_board())
            else:
                print('Error resetting the game.')
        elif action == 'move':
            row = int(input('Enter row (0, 1, or 2): '))
            col = int(input('Enter column (0, 1, or 2): '))
            if game.make_move(row, col):
                print_board(game.get_board())
                if game.check_winner():
                    print(f'Player {'X' if game.check_winner() == 1 else 'O'} wins!')
                    continue
            else:
                print('Invalid move. Try again.')
        elif action == 'exit':
            print('Exiting the game.')
            break

if __name__ == '__main__':
    main()
