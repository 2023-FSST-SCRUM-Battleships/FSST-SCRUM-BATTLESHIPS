import socket

from network.common import *

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

    def coord_input(self):
        """
        This function gets the user input - where the ship should be placed and how
        :param:
        :return: x, y coordinate and rotation
        """
        input_cell = input("> ")
        x, y, rotation = (int(bit) for bit in input_cell.split(" "))
        x, y = x - 1, y - 1
        return [x, y, rotation]


if __name__ == "__main__":
    cl = Client()
    connected = cl.connect()

    while connected:
        # receive message from the server
        server_msg = cl.receive()
        # print(f"[SERVER] {server_msg[2]}")

        # check the type of message received
        if server_msg[1] == 'game_instruction':
            print(f"[SERVER] {server_msg[2]}")
            client_input = int(input("> "))
            cl.send_to_server('game_instruction', client_input)

        elif server_msg[1] == 'ship_id_msg':
            print(f"[SERVER] {server_msg[2]}")
            ship_input = input("> ")
            cl.send_to_server('ship_id_msg', ship_input)

        elif server_msg[1] == 'invalid_shipID_msg':
            print(f"[SERVER] {server_msg[2]}")
            while server_msg[1] == 'invalid_shipID_msg':
                print(f"[SERVER] {server_msg[2]}")
                ship_input = input("> ")
                cl.send_to_server('ship_id_msg', ship_input)
                server_msg = cl.receive()

        elif server_msg[1] == 'ship_coord_msg':
            print(f"[SERVER] {server_msg[2]}")
            coord = cl.coord_input()
            cl.send_to_server('ship_coord_msg', coord)

        elif server_msg[1] == 'invalid_coord_msg':
            print(f"[SERVER] {server_msg[2]}")
            while server_msg[1] == 'invalid__msg':
                print(f"[SERVER] {server_msg[2]}")
                coord = cl.coord_input()
                cl.send_to_server('ship_coord_msg', coord)
                server_msg = cl.receive()

        elif server_msg[1] == 'invalid_instruction':
            print(f"[SERVER] {server_msg[2]}")
            client_input = int(input("> "))
            cl.send_to_server('game_instruction', client_input)

        # if info_msg
        else:
            print(f"[SERVER] {server_msg[2]}")

'''
Game instructions:
0 = EXIT
1 = FINISH
2 = CREATE FLEET
3 = HIT
'''
