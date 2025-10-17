from game import Board, Player, PLAYER_X, TicTacToe, TicTacToeProxy


def player_str(player: Player) -> str:
    return 'X' if player == PLAYER_X else 'O'

def print_board(game: TicTacToe) -> None:
    for row in game.get_board():
        print(' | '.join(['X' if cell == 1 else 'O' if cell == 2 else ' ' for cell in row]))
        print('-' * 9)
    print(f'Current player: {player_str(game.get_current_player())}')


def main() -> None:
    game: TicTacToe = TicTacToeProxy('http://127.0.0.1:5000')
    print_board(game)
    while True:
        action = input('Choose action: [move, reset, exit]: ').strip().lower()
        if action == 'reset':
            if game.reset_game():
                print('Game reset!')
                print_board(game)
            else:
                print('Error resetting the game.')
        elif action == 'move':
            row = int(input('Enter row (0, 1, or 2): '))
            col = int(input('Enter column (0, 1, or 2): '))
            if game.make_move(row, col):
                print_board(game)
                if game.check_winner():
                    print(f'Player {player_str(game.check_winner())} wins!')
                    continue
            else:
                print('Invalid move. Try again.')
        elif action == 'exit':
            print('Exiting the game.')
            break

if __name__ == '__main__':
    main()
