package core

type GameState struct {
	Board      Board
	NextPlayer Player
	Winner     Winner
}
