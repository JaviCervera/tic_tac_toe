package socket

import (
	"bufio"
	"fmt"
	"io"
	"net"
	"slices"
	"sync"
)

type SocketServer struct {
	listener      net.Listener
	quit          chan struct{}
	clients       []net.Conn
	clientsMutex  sync.Mutex
	messages      [][]byte
	messagesMutex sync.Mutex
}

func NewSocketServer(port int) (*SocketServer, error) {
	fmt.Printf("NewSocketServer(%d)\n", port)
	listener, err := net.Listen("tcp", fmt.Sprintf(":%d", port))
	if err != nil {
		return nil, err
	}
	ss := &SocketServer{listener: listener, quit: make(chan struct{})}
	go ss.handleConnections()
	return ss, nil
}

func (ss *SocketServer) Close() {
	fmt.Println("SocketServer.close()")
	close(ss.quit)
	ss.listener.Close()
}

func (ss *SocketServer) handleConnections() {
	for {
		select {
		case <-ss.quit:
			return
		default:
			client, err := ss.listener.Accept()
			if err != nil {
				fmt.Println("Error accepting connection:", err)
				continue
			}
			ss.sendExistingMessages(client)
			go ss.handleClient(client)
		}
	}
}

func (ss *SocketServer) sendExistingMessages(client net.Conn) {
	ss.messagesMutex.Lock()
	defer ss.messagesMutex.Unlock()
	for _, msg := range ss.messages {
		client.Write(msg)
	}
}

func (ss *SocketServer) handleClient(client net.Conn) {
	defer client.Close()
	ss.clientsMutex.Lock()
	ss.clients = append(ss.clients, client)
	ss.clientsMutex.Unlock()

	reader := bufio.NewReader(client)
	for {
		select {
		case <-ss.quit:
			return
		default:
			buf := make([]byte, PacketSize)
			_, err := io.ReadFull(reader, buf)
			if err != nil {
				ss.deleteClient(client)
				return
			}
			ss.addMessage(buf)
			ss.broadcast(buf, client)
		}
	}
}

func (ss *SocketServer) addMessage(message []byte) {
	ss.messagesMutex.Lock()
	defer ss.messagesMutex.Unlock()
	ss.messages = append(ss.messages, message)
}

func (ss *SocketServer) broadcast(message []byte, sender net.Conn) {
	ss.clientsMutex.Lock()
	defer ss.clientsMutex.Unlock()
	for _, client := range ss.clients {
		if client == sender {
			continue
		}
		_, err := client.Write(message)
		if err != nil {
			ss.deleteClient(client)
		}
	}
}

func (ss *SocketServer) deleteClient(client net.Conn) {
	client.Close()
	ss.clientsMutex.Lock()
	index := slices.Index(ss.clients, client)
	if index != -1 {
		ss.clients = append(ss.clients[:index], ss.clients[index+1:]...)
	}
	ss.clientsMutex.Unlock()
}
