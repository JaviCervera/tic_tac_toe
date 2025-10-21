import json

from kafka import KafkaProducer

from .tic_tac_toe import TicTacToeState


class TicTacToeSendStateKafka:
    def __init__(self, url: str, topic: str):
        self._producer = KafkaProducer(url)
        self._topic = topic

    def __call__(self, state: TicTacToeState) -> None:
        self._producer.send(
            self._topic,
            json.dumps(
                {
                    "board": state.board,
                    "current_player": state.current_player,
                    "winner": state.winner,
                }
            ).encode("utf-8"),
        )
        self._producer.flush()
