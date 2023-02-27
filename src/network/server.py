import json
import socket
from enum import Enum


class GuessResponse(Enum):
    MISS = 0
    HIT = 1
    SUNK = 2
    WIN = 3
    INVALID = 4

    @classmethod
    def from_string(cls, string: str):
        if string == "miss":
            return GuessResponse.MISS
        if string == "hit":
            return GuessResponse.HIT
        if string == "sunk":
            return GuessResponse.SUNK
        if string == "win":
            return GuessResponse.WIN
        if string == "invalid":
            return GuessResponse.INVALID

    def __str__(self) -> str:
        if self.value == 0:
            return "miss"
        if self.value == 1:
            return "hit"
        if self.value == 2:
            return "sunk"
        if self.value == 3:
            return "win"
        if self.value == 4:
            return "invalid"


class Connection(object):
    """Uses sockets to communicate with opponent. 'Packet'-format: 'type;data;' """

    def __init__(self, open_as="client", port: int = 5778, address: str = "127.0.0.1"):
        """Opens the communication either as a server or a client"""
        if not address:
            address = "127.0.0.1"
        mode = open_as
        if mode == "client":
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((address, port))
        elif mode == "server":
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((address, port))
            server.listen(1)
            self.connection, ignore = server.accept()
        else:
            raise ValueError("only 'server' and 'client' as arguments allowed. found: " + str(open_as))

    def send_guess(self, x: int, y: int):
        packet = {"mode": "hit", "cell": [x, y]}
        self.connection.send(json.dumps(packet).encode())

    def await_guess(self) -> tuple[int, int] | None:
        """this method blocks, until a guess was received (or an error occurred)"""
        data = self.connection.recv(512).decode()
        packet = json.loads(data)
        mode = packet.get("mode")
        if mode != "hit":
            return None
        cell = packet.get("cell")
        return cell[0], cell[1]

    def send_response(self, response: GuessResponse):
        packet = {"mode": "response", "response": str(response)}
        self.connection.send(json.dumps(packet).encode())

    def await_response(self):
        """this method blocks, until a FieldState was received (or an error occurred)"""
        data = self.connection.recv(512).decode()
        packet = json.loads(data)
        mode = packet.get("mode")
        if mode != "response":
            return None
        response = GuessResponse.from_string(packet.get("response"))
        return response

    def await_done(self):
        """this method blocks, until a "done" was received (or an error occurred)"""
        data = self.connection.recv(512).decode()
        packet = json.loads(data)
        mode = packet.get("mode")
        if mode != "done":
            return None

    def send_done(self):
        packet = {"mode": "done"}
        self.connection.send(json.dumps(packet).encode())

    def await_both_done(self):
        self.send_done()
        self.await_done()
