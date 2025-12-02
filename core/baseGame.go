package core

type BaseGame struct {
	State         GameState
	CurrentPlayer Player
	Client        Client
}

func (game *BaseGame) GameState() GameState {
	return game.State
}

func (game *BaseGame) Update() {
	receivedState := game.Client.ReceiveState()
	for receivedState != nil {
		game.State = *receivedState
		receivedState = game.Client.ReceiveState()
	}
}

func (game *BaseGame) Move(movement Movement) bool {
	if game.State.NextPlayer == game.CurrentPlayer {
		newState := performMovement(game.State, movement)
		if newState != nil {
			game.State = *newState
			game.Client.SendState(game.State)
		}
		return true
	}
	return false
}

func (game *BaseGame) GameOver() bool {
	return game.State.Winner != nil
}

func performMovement(state GameState, movement Movement) *GameState {
	if state.Board[movement.row][movement.col] != nil || state.Winner != nil {
		return nil
	}
	state.Board[movement.row][movement.col] = &state.NextPlayer
	return &GameState{
		state.Board,
		nextPlayer(state.NextPlayer),
		checkWinner(state.Board),
	}
}

func nextPlayer(currentPlayer Player) Player {
	if currentPlayer == PlayerX {
		return Player0
	}
	return PlayerX
}

func checkWinner(board Board) Winner {
	if !hasEmptyCells(board) {
		return DrawGame
	}
	for i := range board {
		if (board[i][0] == board[i][1] && board[i][1] == board[i][2] && board[i][0] != nil) ||
			(board[0][i] == board[1][i] && board[1][i] == board[2][i] && board[0][i] != nil) {
			return &board[i][0]
		}
	}
	if (board[0][0] == board[1][1] && board[1][1] == board[2][2] && board[0][0] != nil) ||
		(board[0][2] == board[1][1] && board[1][1] == board[2][0] && board[0][2] != nil) {
		return &board[1][1]
	}
	return nil
}

func hasEmptyCells(board Board) bool {
	for _, row := range board {
		for _, cell := range row {
			if cell == nil {
				return true
			}
		}
	}
	return false
}
