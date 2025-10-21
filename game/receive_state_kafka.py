import json

from kafka import KafkaConsumer

from .tic_tac_toe import TicTacToeState


class TicTacToeReceiveStateKafka:
    def __init__(self, url: str, topic: str):
        self._consumer = KafkaConsumer(
            topic,
            bootstrap_servers=url,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id=f"{topic}-group",
        )

    def __call__(self) -> TicTacToeState | None:
        for message in self._consumer:
            json_state = json.loads(message.value.decode("utf-8"))
            return TicTacToeState(
                board=json_state["board"],
                current_player=json_state["current_player"],
                winner=json_state["winner"],
            )
        return None
