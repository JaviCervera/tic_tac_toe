import json

from kafka import KafkaConsumer

from game.tic_tac_toe import TicTacToeState


class TicTacToeReceiveStateKafka:
    def __init__(self, url: str, topic: str):
        self._consumer = KafkaConsumer(
            topic,
            bootstrap_servers=url,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )

    def __call__(self) -> TicTacToeState | None:
        state: TicTacToeState | None = None
        topics = self._consumer.poll(timeout_ms=5)
        for _, messages in topics.items():
            for message in messages:
                json_state = json.loads(message.value.decode("utf-8"))
                state = TicTacToeState(
                    board=json_state["board"],
                    current_player=json_state["current_player"],
                    winner=json_state["winner"],
                )
        return state
