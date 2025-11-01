import socket


class PacketStream:
    PACKET_SIZE = 11

    def __init__(self, client: socket.socket):
        self._client = client
        self._buffer = bytearray()
        self._client.setblocking(False)

    def read_packet(self) -> bytes | None:
        try:
            self._buffer.extend(self._client.recv(self.PACKET_SIZE))
        except BlockingIOError:
            pass
        if len(self._buffer) >= self.PACKET_SIZE:
            packet = self._buffer[: self.PACKET_SIZE]
            del self._buffer[: self.PACKET_SIZE]
            return packet
        return None
