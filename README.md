# Tic Tac Toe

A very simple multiplayer Go implementation of Tic Tac Toe wich can be played in local mode or with a client-server connection.

There is a *config.json* file at the root to configure the client:
* To run in local mode, set `local` to `true`.
* To run with server, set `sockets_host` to point to a given host:port (for example, `localhost:1234`).

In local mode, `go run main.go` must be triggered once to start playing (or compile the file once and then launch the executable). Both players will take turns to play on the same machine.

In server mode, two instances must be launched, selecting "X" on one to create a game (this instance will contain the server and one client for player X), and "O" on the other to join the existing server and create one client for player O.
