package local

import "tic_tac_toe/core"

type LocalGame struct {
	core.BaseGame
}

func NewLocalGame() *LocalGame {
	return &LocalGame{
		BaseGame: core.BaseGame{
			State:  core.NewGameState(),
			Player: core.PlayerX,
			Client: &LocalClient{},
		},
	}
}

func (game *LocalGame) Move(movement core.Movement) bool {
	result := game.BaseGame.Move(movement)
	game.Player = game.State.NextPlayer
	return result
}

func (game *LocalGame) Cleanup() {}

func (game *LocalGame) CurrentPlayer() core.Player {
	return game.Player
}
