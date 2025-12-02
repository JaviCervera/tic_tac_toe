package core

type Client interface {
	SendState(state GameState)
	ReceiveState() *GameState
	Close()
}
