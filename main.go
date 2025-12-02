package main

import (
	"encoding/json"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
	"tic_tac_toe/core"
	"tic_tac_toe/local"
	"tic_tac_toe/remote"
	"tic_tac_toe/window"
)

func main() {
	config := loadConfig("config.json")
	game := createGame(config, core.NoPlayer)
	window.OpenWindow()
	for !window.ShouldCloseWindow() {
		if game == nil {
			selPlayer := window.SelectedPlayer()
			if selPlayer != nil {
				game = createGame(config, *selPlayer)
			}
			window.DrawWelcomeScreen()
		} else {
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
				game = createGame(config, core.NoPlayer)
			}
		}
	}
	window.CloseWindow()
	game.Cleanup()
}

type Config struct {
	Local       bool   `json:"local"`
	SocketsHost string `json:"sockets_host"`
}

func loadConfig(filename string) Config {
	jsonFile, err := os.Open(filename)
	if err != nil {
		return Config{Local: true}
	}
	defer jsonFile.Close()

	bytes, _ := io.ReadAll(jsonFile)
	var config Config
	json.Unmarshal(bytes, &config)
	return config
}

func createGame(config Config, player core.Player) core.Game {
	if config.Local {
		return local.NewLocalGame()
	}
	if player != core.NoPlayer {
		hostSplit := strings.Split(config.SocketsHost, ":")
		if len(hostSplit) != 2 {
			return nil
		}
		host := hostSplit[0]
		port, err := strconv.Atoi(hostSplit[1])
		if err != nil {
			return nil
		}
		game, err := remote.NewRemoteGame(host, port, player)
		if err != nil {
			panic(err)
		}
		return game
	}
	return nil
}
