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

    def receive(self, conn) -> tuple[bool, any, any]:
        """
        receives a packet from client
        :return:
        """

        try:
            # accu = collects all the bytes aka "buffer" -> accu is for receiving more than the recv size
            accu = bytearray()

            while True:
                data = conn.recv(512)
                print(data)
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

        except IOError as Err:
            print(Err)
            return False, None, None

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        while connected:
            self.send_to_client(conn, "info_msg", "Welcome to the Battleship game!\n"
                                                  "You need to create your fleet!\n"
                                                  "Available ships: Carrier 1x, Submarine 2x and Destroyer 3x\n"
                                                  "Game instructions: \n"
                                                  "3 = EXIT\n"
                                                  "4 = CREATE FLEET\n"
                                                  "5 = HIT"
                                )

            while True:
                self.send_to_client(conn, 'game_instruction', 'Input instruction: ')
                client_msg = self.receive(conn)

                # if message received
                if client_msg[0]:
                    # checks for the type of input
                    if client_msg[1] == 'game_instruction':
                        # if input is EXIT
                        if client_msg[2] == 3:
                            connected = False
                            break

                        # if user wants to create fleet
                        elif client_msg[2] == 4:
                            # until the user places all 6 boats
                            while ship_count > 0:
                                self.send_to_client(conn, 'ship_id_msg', 'Input ship: ')
                                ship_type = self.receive(conn)

                                # in handle_message catching invalid input - returns True/False
                                while not handle_message(ship_type[1:]):
                                    self.send_to_client(conn, 'invalid_shipID_msg', 'Invalid input! Please try again:')
                                    ship_type = self.receive(conn)
                                    handle_message(ship_type[1:])
                                else:
                                    self.send_to_client(conn, 'info_msg', 'Message received')
                                    handle_message(ship_type[1:])

                                self.send_to_client(conn, 'ship_coord_msg', 'Please enter the coordinates & rotation: ')
                                coord = self.receive(conn)
                                while not handle_message(coord[1:]):
                                    self.send_to_client(conn, 'invalid_coord_msg', 'Invalid input! Please try again: ')
                                    coord = self.receive(conn)
                                    handle_message(coord[1:])

                                self.send_to_client(conn, 'board_status', my_board)

                        '''if ship_type[2] == 3:
                            break

                        elif client_msg[2] == 5:
                            pass'''

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
