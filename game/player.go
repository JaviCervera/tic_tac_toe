package game

type Player int

const (
	PlayerX Player = iota
	Player0
)

func PlayerStr(player Player) string {
	return (player == PlayerX) ? "X" : "0"
}
