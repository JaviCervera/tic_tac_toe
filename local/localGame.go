package local

import "tic_tac_toe/core"

type LocalGame struct {
	core.BaseGame
}

func (game *LocalGame) Move(movement core.Movement) bool {
	result := game.BaseGame.Move(movement)
	game.CurrentPlayer = game.State.NextPlayer
	return result
}

func NewLocalGame() LocalGame {
	return LocalGame{}
}
