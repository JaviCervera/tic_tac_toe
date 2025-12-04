package socket

import (
	"bufio"
	"fmt"
	"io"
	"net"
	"tic_tac_toe/core"
)

type SocketClient struct {
	conn  net.Conn
	state chan core.GameState
	quit  chan struct{}
}

func NewSocketClient(host string, port int) (*SocketClient, error) {
	conn, err := net.Dial("tcp", fmt.Sprintf("[%s]:%d", host, port))
	if err != nil {
		return nil, err
	}
	client := &SocketClient{conn: conn, state: make(chan core.GameState), quit: make(chan struct{})}
	go client.readMessages()
	return client, nil
}

func (sc *SocketClient) SendState(state core.GameState) {
	fmt.Printf("SendState(%s)\n", state)
	_, err := sc.conn.Write(stateToBytes(state))
	if err != nil {
		fmt.Println("SendSate() failed")
	}
}

func (sc *SocketClient) ReceiveState() *core.GameState {
	select {
	case state := <-sc.state:
		fmt.Printf("ReceiveState() -> %s\n", state)
		return &state
	default:
		return nil
	}
}

func (sc *SocketClient) Close() {
	sc.conn.Close()
}

func (sc *SocketClient) readMessages() {
	reader := bufio.NewReader(sc.conn)
	for {
		select {
		case <-sc.quit:
			return
		default:
			buf := make([]byte, PacketSize)
			_, err := io.ReadFull(reader, buf)
			if err != nil {
				return
			}
			sc.state <- bytesToState(buf)
		}
	}
}

func stateToBytes(state core.GameState) []byte {
	arr := make([]byte, core.GridSize*core.GridSize+2)
	for i := 0; i < core.GridSize; i++ {
		for j := 0; j < core.GridSize; j++ {
			arr[i*core.GridSize+j] = byte(state.Board[i][j])
		}
	}
	arr[core.GridSize*core.GridSize] = byte(state.NextPlayer)
	arr[core.GridSize*core.GridSize+1] = byte(state.Winner)
	return arr
}

func bytesToState(data []byte) core.GameState {
	board := core.NewBoard()
	for i := 0; i < core.GridSize; i++ {
		for j := 0; j < core.GridSize; j++ {
			board[i][j] = core.Player(data[i*core.GridSize+j])
		}
	}
	return core.GameState{
		Board:      board,
		NextPlayer: core.Player(data[core.GridSize*core.GridSize]),
		Winner:     core.Player(data[core.GridSize*core.GridSize+1]),
	}
}
