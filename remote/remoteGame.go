package remote

import (
	"tic_tac_toe/core"
	"tic_tac_toe/socket"
)

type RemoteGame struct {
	core.BaseGame
	server *socket.SocketServer
}

func NewRemoteGame(host string, port int, player core.Player) (*RemoteGame, error) {
	var server *socket.SocketServer
	if player == core.PlayerX {
		var err error
		server, err = socket.NewSocketServer(port)
		if err != nil {
			return nil, err
		}
	}
	client, err := socket.NewSocketClient(host, port)
	if err != nil {
		return nil, err
	}
	return &RemoteGame{
		BaseGame: core.BaseGame{
			State:  core.NewGameState(),
			Player: player,
			Client: client,
		},
		server: server,
	}, nil
}

func (game *RemoteGame) Cleanup() {
	if game.server != nil {
		game.server.Close()
	}
}

func (game *RemoteGame) CurrentPlayer() core.Player {
	return game.Player
}
