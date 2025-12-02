package window

import (
	"fmt"
	"tic_tac_toe/core"

	rl "github.com/gen2brain/raylib-go/raylib"
)

const winWidth = 600
const winHeight = 600
const cellSize = winWidth / core.GridSize

func OpenWindow() {
	rl.SetTraceLogLevel(rl.LogNone)
	rl.InitWindow(winWidth, winHeight, "Tic Tac Toe")
	rl.SetTargetFPS(60)
}

func CloseWindow() {
	rl.CloseWindow()
}

func ShouldCloseWindow() bool {
	return rl.WindowShouldClose()
}

func SelectedPlayer() *core.Player {
	var player core.Player
	if rl.IsKeyPressed(rl.KeyX) {
		player = core.PlayerX
	} else if rl.IsKeyPressed(rl.KeyO) {
		player = core.Player0
	} else {
		return nil
	}
	return &player
}

func SelectedMovement() *core.Movement {
	if rl.IsMouseButtonPressed(rl.MouseButtonLeft) {
		mouseX := rl.GetMouseX()
		mouseY := rl.GetMouseY()
		col := mouseX / cellSize
		row := mouseY / cellSize
		return &core.Movement{Row: int(row), Col: int(col)}
	}
	return nil
}

func SelectedRestart() bool {
	return rl.IsMouseButtonPressed(rl.MouseButtonRight)
}

func DrawGameState(state core.GameState, localPlayer core.Player) {
	rl.BeginDrawing()
	rl.ClearBackground(rl.RayWhite)
	drawBoard(state.Board)
	if state.Winner != nil {
		message := ""
		if state.Winner == core.DrawGame {
			message = "It's a draw!"
		} else {
			message = fmt.Sprintf("Player %s wins!", core.PlayerStr(state.Winner.(core.Player)))
		}
		rl.DrawText(message, winWidth/2-100, winHeight/2-20, 20, rl.DarkGray)
		rl.DrawText("Click right mouse button to reset", winWidth/2-100, winHeight/2, 20, rl.DarkGray)
	} else {
		message := fmt.Sprintf("Player: %s -- Turn: %s", core.PlayerStr(localPlayer), core.PlayerStr(state.NextPlayer))
		rl.DrawText(message, (winWidth-rl.MeasureText(message, 20))/2, winHeight-32, 20, rl.DarkGray)
	}
	rl.EndDrawing()
}

func drawBoard(board core.Board) {
	for rowIdx, row := range board {
		for colIdx, cell := range row {
			x := int32(colIdx * cellSize)
			y := int32(rowIdx * cellSize)
			switch cell {
			case core.PlayerX:
				rl.DrawLine(x+20, y+20, x+cellSize-20, y+cellSize-20, rl.Red)
				rl.DrawLine(x+cellSize-20, y+20, x+20, y+cellSize-20, rl.Red)
			case core.Player0:
				rl.DrawCircle(x+cellSize/2, y+cellSize/2, cellSize/2-20, rl.Blue)
			}
		}
	}
}
