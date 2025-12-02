package core

type GameState struct {
	Board      Board
	NextPlayer Player
	Winner     Player
}

func NewGameState() GameState {
	return GameState{
		Board:      newBoard(),
		NextPlayer: PlayerX,
		Winner:     NoPlayer,
	}
}

func newBoard() Board {
	var board Board
	for i := range board {
		for j := range board[i] {
			board[i][j] = NoPlayer
		}
	}
	return board
}
