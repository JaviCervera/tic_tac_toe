import logging

from ..client import Client
from ..config import Config
from ..constants import PLAYER_X
from ..kafka.kafka_client import KafkaClient
from ..logged.logged_client import LoggedClient
from ..player import Player
from ..sockets.sockets_client import SocketsClient
from ..sockets.sockets_server import SocketsServer
from ..tic_tac_toe_game import TicTacToeGame


class RemoteGame(TicTacToeGame):
    def __init__(self, config: Config, player: Player, logger: logging.Logger):
        self._server: SocketsServer | None = None
        if config.sockets_host:
            host_split = config.sockets_host.split(":")
            host = host_split[-2]
            port = int(host_split[-1])
            if player == PLAYER_X:
                self._server = SocketsServer(port, logger)
            client: Client = SocketsClient(host, port)
        elif config.kafka_url and config.kafka_topic:
            client = KafkaClient(
                config.kafka_url, config.kafka_topic, player == PLAYER_X
            )
        else:
            raise RuntimeError("Need to specify connection details in config")
        super().__init__(player, LoggedClient(client, logger))

    def close(self) -> None:
        super().close()
        if self._server:
            self._server.close()
