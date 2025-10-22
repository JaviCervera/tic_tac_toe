import json

from kafka import KafkaConsumer, KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import UnknownTopicOrPartitionError

from game.client import Client
from game.tic_tac_toe_state import TicTacToeState


class KafkaClient(Client):
    def __init__(self, url: str, topic: str) -> None:
        self._url = url
        self._topic = topic
        self._delete_topic()
        self._create_topic()
        self._producer = KafkaProducer(bootstrap_servers=url)
        self._consumer = KafkaConsumer(
            topic,
            bootstrap_servers=url,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )

    def send_state(self, state: TicTacToeState) -> None:
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

    def receive_state(self) -> TicTacToeState | None:
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

    def _delete_topic(self) -> None:
        client = KafkaAdminClient(bootstrap_servers=self._url)
        try:
            client.delete_topics([self._topic])
        except UnknownTopicOrPartitionError:
            pass
        finally:
            client.close()

    def _create_topic(self) -> None:
        client = KafkaAdminClient(bootstrap_servers=self._url)
        topic = NewTopic(
            name=self._topic,
            num_partitions=1,
            replication_factor=1,
        )
        try:
            client.create_topics([topic])
        finally:
            client.close()
