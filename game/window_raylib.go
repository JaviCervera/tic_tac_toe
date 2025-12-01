package game

import rl "github.com/gen2brain/raylib-go/raylib"

const winWidth int32 = 600
const winHeight int32 = 600

func OpenWindow() {
	rl.SetTraceLogLevel(rl.LogNone)
	rl.InitWindow(winWidth, winHeight, "Tic Tac Toe")
	rl.SetTargetFPS(60)
}

func CloseWindow() {
	rl.CloseWindow()
}
