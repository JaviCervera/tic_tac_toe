package core

type BaseGame struct {
	State  GameState
	Player Player
	Client Client
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
	if game.State.NextPlayer == game.Player {
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
	if state.Board[movement.Row][movement.Col] != NoPlayer || state.Winner != nil {
		return nil
	}
	state.Board[movement.Row][movement.Col] = state.NextPlayer
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
		if hasSamePlayer(board[i][0], board[i][1], board[i][2]) {
			return board[i][0]
		}
		if hasSamePlayer(board[0][i], board[1][i], board[2][i]) {
			return board[0][i]
		}
	}
	if hasSamePlayer(board[0][0], board[1][1], board[2][2]) {
		return board[0][0]
	}
	if hasSamePlayer(board[0][2], board[1][1], board[2][0]) {
		return board[0][2]
	}
	return nil
}

func hasEmptyCells(board Board) bool {
	for _, row := range board {
		for _, cell := range row {
			if cell == NoPlayer {
				return true
			}
		}
	}
	return false
}

func hasSamePlayer(cell1 Player, cell2 Player, cell3 Player) bool {
	return cell1 != NoPlayer && cell1 == cell2 && cell2 == cell3
}
