package game

type Player int

const (
	PlayerX Player = iota
	Player0
)

func PlayerStr(player Player) string {
	if player == PlayerX {
		return "X"
	} else {
		return "0"
	}
}
