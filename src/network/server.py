import socket
import threading
import select
from common import *
from src.database.account_manager import *

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
FORMAT = "utf-8"


class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = {}
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
            # blocks, until data is readable or a socket is broken
            # self.connections.values() -> nur die gefilterten connections -> also freie connections
            # conn die im spiel sind in zusätz. liste speichern und die allgemeine liste dadurch filtern

            readable, writable, exceptional = select.select(self.connections.values(), [], self.connections.values())
            # TODO check exceptional (probably disconnected) sockets
            # alle die exceptional sind aus der connections rausschmeißen
            client = readable[0]

            # accu = collects all the bytes aka "buffer" -> accu is for receiving more than the recv size
            accu = ""

            curly_braces_count = 0
            in_string = False
            while True:
                char = client.recv(1).decode(FORMAT)
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

    def handle_client(self, conn1, conn2, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        while connected:
            # var für die conn die dran ist
            # andere con wird nicht beachtet
            client_msg = self.receive()
            if client_msg[0]:
                self.send_to_client(conn, 'info_msg', 'Message received')
                if client_msg[1] == 'used_coord':
                    placed_ships = client_msg[2]

            print(f'["CLIENT"] {client_msg[2]} ')

        conn.close()


if __name__ == "__main__":
    serv = Server()
    serv.server.bind(ADDR)
    serv.server.listen()
    print(f"[LISTENING] Server is listening on {ADDR}")
    # TODO: Login

    # Lobby
    threading.Thread(target=handle_lobby, args=(serv,)).start()


    # in Lobby stats anzeigen

    def handle_lobby(server):
        pass


    # listen to players, who they want to play with ["kilian", "Matze"]
    # matchmaking - access auf connection[]
    # thread = threading.Thread(target=serv.handle_game, args=(conn1, conn2, addr))
    # thread.start()
    # print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    while True:
        conn, addr = serv.server.accept()
        serv.connections.append(conn)

# people = Account.select()
# TODO: broadcast the list of accounts to client
