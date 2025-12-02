package local

import "tic_tac_toe/core"

type LocalClient struct {
	queue     []core.GameState
	nextIndex int
}

func (client *LocalClient) SendState(state core.GameState) {
	client.queue = append(client.queue, state)
}

func (client *LocalClient) ReceiveState() *core.GameState {
	if client.nextIndex < len(client.queue) {
		client.nextIndex++
		return &client.queue[client.nextIndex-1]
	}
	return nil
}

func (client *LocalClient) Close() {
}
