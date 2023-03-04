import socket

from network.common import *

SERVER_ADDRESS = "aether.net.co"


class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, server_address: str = SERVER_ADDRESS) -> bool:
        """
        connects to a certain server-address
        :param server_address:
        :return:
        """

        try:
            self.socket.connect((server_address, SERVER_PORT))
            return True

        except IOError:
            return False

    def send(self, _type: str, data: any or None = None) -> bool:
        """
        sends a packet with a type & its data to server
        :param _type:
        :param data:
        :return:
        """

        try:
            self.socket.send(encode_packet(_type, data).encode("utf-8"))

        except IOError:
            return False

    def receive(self) -> tuple[bool, any, any]:
        """
        receives a packet from server
        :return:
        """

        try:
            # accu = collects all the bytes aka "buffer" -> accu is for receiving more than the recv size
            accu = bytearray()

            while True:
                data = self.socket.recv(512)
                if not data:
                    # end of sent data / no bytes received
                    break

                for byte in data:
                    accu.append(byte)

                if len(data) < 512:
                    # end of sent data but not receive size
                    break

            _type, data = decode_packet(accu.decode("utf-8"))
            return True, _type, data

        except IOError:
            return False, None, None
