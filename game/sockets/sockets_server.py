import logging
import queue
import socket
import threading

from .packet_stream import PacketStream


class SocketsServer:
    def __init__(self, port: int, logger: logging.Logger):
        logger.info(f"SocketsServer.init({port})")
        self._logger = logger
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.setblocking(False)
        self._server.bind(("0.0.0.0", port))
        self._server.listen(2)
        self._dispatched_queue: queue.Queue[bytes] = queue.Queue()
        self._client_threads: list[threading.Thread] = []
        self._client_sockets: list = []
        self._stop_event = threading.Event()
        self._server_thread = threading.Thread(target=self._accept_connection)
        self._server_thread.start()

    def close(self) -> None:
        self._logger.info("SocketsServer.close()")
        self._stop_event.set()
        for thread in self._client_threads:
            thread.join()
        self._server.close()
        self._logger.info("* Server closed")

    def _accept_connection(self) -> None:
        while not self._stop_event.is_set():
            try:
                client_socket, addr = self._server.accept()
                client_thread = threading.Thread(
                    target=self._handle_client_packets,
                    args=(client_socket, PacketStream(client_socket)),
                )
                client_thread.start()
                self._client_threads.append(client_thread)
                self._client_sockets.append(client_socket)

                # Send already dispatched packets to new client
                with self._dispatched_queue.mutex:
                    msg_list = list(self._dispatched_queue.queue)
                for msg in msg_list:
                    client_socket.send(msg)
            except BlockingIOError:
                pass

    def _handle_client_packets(
        self, socket: socket.socket, stream: PacketStream
    ) -> None:
        while not self._stop_event.is_set():
            try:
                packet = stream.read_packet()
                if packet is not None:
                    # Send packet to all connected clients
                    for client_socket in self._client_sockets:
                        client_socket.send(packet)
                    self._dispatched_queue.put(packet)
            except ConnectionResetError:
                break
        self._client_sockets.remove(socket)
        socket.close()
