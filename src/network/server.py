import socket
import threading
from common import *

from msg_handler import *

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
FORMAT = "utf-8"


class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[STARTING] Server is starting...")

    def send_to_client(self, conn, _type: str, data: any or None = None) -> bool:
        """
        sends a packet with a type & its data to client
        :param _type:
        :param data:
        :return:
        """

        try:
            conn.send(encode_packet(_type, data).encode(FORMAT))

        except IOError:
            return False

    def receive(self) -> tuple[bool, any, any]:
        """
        receives a packet from server
        :return:
        """

        try:
            # accu = collects all the bytes aka "buffer" -> accu is for receiving more than the recv size
            accu = ""

            curly_braces_count = 0
            in_string = False
            while True:
                char = self.client.recv(1).decode(FORMAT)
                if not char:
                    # end of sent data / no bytes received
                    break

                accu += char

                if char == '{' and not in_string:  # open braces
                    curly_braces_count += 1
                elif char == '}' and not in_string:  # close braces
                    curly_braces_count -= 1
                    if curly_braces_count == 0:  # last brace closed, packet done
                        break
                elif char == '"' or char == "'":
                    in_string = not in_string

            _type, data = decode_packet(accu)
            return True, _type, data

        except IOError:
            return False, None, None

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        while connected:
            client_msg = self.receive()
            print(f'["CLIENT"] {client_msg} ')
            self.send_to_client(conn, 'info_msg', 'Message received')

        conn.close()


if __name__ == "__main__":
    serv = Server()
    serv.server.bind(ADDR)
    serv.server.listen()
    print(f"[LISTENING] Server is listening on {ADDR}")

    while True:
        conn, addr = serv.server.accept()
        thread = threading.Thread(target=serv.handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
