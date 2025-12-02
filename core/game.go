package core

const DrawGame = -1

type Game interface {
	GameState() GameState
	Update()
	Move(movement Movement) bool
	GameOver() bool
	CurrentPlayer() Player
	Cleanup()
}
