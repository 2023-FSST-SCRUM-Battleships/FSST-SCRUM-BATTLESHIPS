import socket
from src.network.common import *
from msg_handler import *

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self) -> bool:
        """
        connects to a certain server-address
        :return:
        """

        try:
            self.client.connect(ADDR)
            print(f"[CONNECTED] {ADDR}")
            return True

        except IOError:
            return False

    def send_to_server(self, _type: str, data: any or None = None) -> bool:
        """
        sends a packet with a type & its data to server
        :param _type:
        :param data:
        :return:
        """

        try:
            self.client.send(encode_packet(_type, data).encode(FORMAT))

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
                data = self.client.recv(512)
                if not data:
                    # end of sent data / no bytes received
                    break

                for byte in data:
                    accu.append(byte)

                if len(data) < 512:
                    # end of sent data but not receive size
                    break

            _type, data = decode_packet(accu.decode(FORMAT))
            return True, _type, data

        except IOError:
            return False, None, None


if __name__ == "__main__":
    cl = Client()
    connected = cl.connect()
    while connected:
        # receive message from the server
        server_msg = cl.receive()
        print(f"[SERVER] {server_msg[2]}")

'''
Game instructions:
0 = EXIT
1 = CREATE FLEET
2 = HIT
'''
