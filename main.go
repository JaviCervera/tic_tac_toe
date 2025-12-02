package main

import (
	"fmt"
	"tic_tac_toe/core"
	"tic_tac_toe/local"
	"tic_tac_toe/window"
)

func main() {
	game := createGame()
	window.OpenWindow()
	for !window.ShouldCloseWindow() {
		if !game.GameOver() {
			game.Update()
			movement := window.SelectedMovement()
			if movement != nil {
				if !game.Move(*movement) {
					fmt.Println("Invalid movement")
				}
			}
		}
		window.DrawGameState(game.GameState(), game.CurrentPlayer())
		if game.GameOver() && window.SelectedRestart() {
			game.Cleanup()
			game = createGame()
		}
	}
	window.CloseWindow()
	game.Cleanup()
}

func createGame() core.Game {
	return local.NewLocalGame()
}
