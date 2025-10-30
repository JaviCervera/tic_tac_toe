import json
import threading
import queue

from kafka import KafkaConsumer, KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import UnknownTopicOrPartitionError

from ..client import Client
from ..tic_tac_toe_state import TicTacToeState


class KafkaClient(Client):
    def __init__(self, url: str, topic: str, recreate_topic: bool) -> None:
        self._url = url
        self._topic = topic
        if recreate_topic:
            self._delete_topic()
            self._create_topic()
        self._producer = KafkaProducer(bootstrap_servers=url)
        self._consumer = KafkaConsumer(
            topic,
            bootstrap_servers=url,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )
        self._queue: queue.Queue = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._consume_messages)
        self._thread.start()

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
        while not self._queue.empty():
            state = self._queue.get()
        return state

    def close(self) -> None:
        self._stop_event.set()
        self._thread.join()
        self._consumer.close()
        self._producer.close()

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

    def _consume_messages(self) -> None:
        while not self._stop_event.is_set():
            messages = self._consumer.poll(timeout_ms=5.0)
            for tp, message_list in messages.items():
                for message in message_list:
                    json_state = json.loads(message.value.decode("utf-8"))
                    state = TicTacToeState(
                        board=json_state["board"],
                        current_player=json_state["current_player"],
                        winner=json_state["winner"],
                    )
                    self._queue.put(state)
