package core

const DrawGame = 2 // 0 and 1 and PlayerX and Player0 respectively

type Game interface {
	GameState() GameState
	Update()
	Move(movement Movement) bool
	GameOver() bool
	CurrentPlayer() Player
	Cleanup()
}
