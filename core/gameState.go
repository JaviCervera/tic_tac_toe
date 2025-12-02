package core

import "fmt"

type GameState struct {
	Board      Board
	NextPlayer Player
	Winner     Player
}

func NewGameState() GameState {
	return GameState{
		Board:      NewBoard(),
		NextPlayer: PlayerX,
		Winner:     NoPlayer,
	}
}

func (state GameState) String() string {
	return fmt.Sprintf("GameState{Board:%s,NextPlayer:%s,Winner:%s}", state.Board, state.NextPlayer, state.Winner)
}
