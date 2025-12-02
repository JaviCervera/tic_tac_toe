package core

type Player int

const (
	NoPlayer Player = iota
	PlayerX
	Player0
)

func PlayerStr(player Player) string {
	if player == PlayerX {
		return "X"
	} else {
		return "0"
	}
}
