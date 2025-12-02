package core

type Player int

const (
	NoPlayer Player = iota
	PlayerX
	PlayerO
)

func (player Player) String() string {
	switch player {
	case PlayerX:
		return "X"
	case PlayerO:
		return "O"
	}
	return "-"
}
