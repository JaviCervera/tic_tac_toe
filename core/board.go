package core

import (
	"strings"
)

const GridSize = 3

type Board [GridSize][GridSize]Player

func NewBoard() Board {
	var board Board
	for i := range board {
		for j := range board[i] {
			board[i][j] = NoPlayer
		}
	}
	return board
}

func (board Board) String() string {
	var builder strings.Builder
	builder.WriteString("Board{")
	for i := range board {
		if i != 0 {
			builder.WriteString(",")
		}
		builder.WriteString("[")
		for j := range board[i] {
			if j != 0 {
				builder.WriteString(",")
			}
			builder.WriteString(board[i][j].String())
		}
		builder.WriteString("]")
	}
	builder.WriteString("}")
	return builder.String()
}
