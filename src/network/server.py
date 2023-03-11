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

    def receive_from_connection(self, client):
        try:
            # accu = collects all the bytes aka "buffer" -> accu is for receiving more than the recv size
            accu = ""

            curly_braces_count = 0
            string_char = None
            last_char = None
            while True:
                char = client.recv(1).decode(FORMAT)
                if not char:
                    # end of sent data / no bytes received
                    break

                accu += char

                if char == '{' and not string_char:  # open braces
                    curly_braces_count += 1
                elif char == '}' and not string_char:  # close braces
                    curly_braces_count -= 1
                    if curly_braces_count == 0:  # last brace closed, packet done
                        break
                elif char == '"' or char == "'":
                    if not last_char == "\\":
                        if string_char is None:
                            string_char = char
                        else:
                            string_char = None
                last_char = char

            _type, data = decode_packet(accu)
            return True, _type, data

        except IOError:
            return False, None, None

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
            return self.receive_from_connection(client)
        except IOError:
            return False, None, None

    def handle_game(self, conn1, conn2):
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

    def handle_login(self, con):
        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        while connected:
            client_msg = self.receive()
            if client_msg[1] == 'login_msg':
                username, password = client_msg[2]
                user = AuthHelper.check_credentials(username, password)
                self.send_to_client(con, 'login_msg', user is not None)
                if user:
                    return user

            if client_msg[1] == 'register_msg':
                username, password = client_msg[2]
                user = AuthHelper.create_account(username, password)
                self.send_to_client(con, 'register_msg', user is not None)
                if user:
                    return user


# show stats in Lobby
def handle_lobby(server):
    selected_player = {}
    while True:
        readable, writable, exceptional = select.select(server.connections.values(), [], server.connections.values())
        con = readable[0]
        username = [key for key in server.connections if server.connections[key] == con][0]
        received, msg_type, msg = server.receive_from_connection(con)

        if msg_type == 'disconnect_msg':
            server.connections.pop(username)
            # broadcast to the clients that this player disconnected
            for client in server.connections.values():
                server.send_to_client(client, 'player_disconnect', username)
            for player in selected_player:
                selected_player[player].remove(username)
            selected_player.pop(username)

        if msg_type == 'play_with_msg':
            if username not in selected_player:
                selected_player[username] = []
            if str(msg[1]) == 'True':  # because we don't know if it is bool or str
                selected_player[username].append(msg[0])
            else:
                if msg[0] in selected_player[username]:
                    selected_player[username].remove(msg[0])

            if msg[0] not in selected_player:
                selected_player[msg[0]] = []
            if username in selected_player[msg[0]] and msg[0] in selected_player[username]:
                # target(msg[0]) player selected current player
                con2 = server.connections[msg[0]]
                thread = threading.Thread(target=server.handle_game, args=(con, con2))
                thread.start()
                # TODO: mark players as not in loby
                # print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == "__main__":
    serv = Server()
    serv.server.bind(ADDR)
    serv.server.listen()
    print(f"[LISTENING] Server is listening on {ADDR}")

    # Lobby
    threading.Thread(target=handle_lobby, args=(serv,)).start()

    while True:
        conn, addr = serv.server.accept()
        user = serv.handle_login(conn)
        if not user:
            conn.close()
            continue

        # save the username and the connection in the dict
        serv.connections[user.username] = conn
        # TODO: send the list of accounts to client when he connects
        # TODO: when new client connects, send the new list of conn to all clients


