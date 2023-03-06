from fleet_creator import *

type_of_ship = None
# the total number of ships available
ship_count = 6


# here will all the necessary functions for the game be called
def handle_message(msg):
    if msg[0] == 'ship_id_msg':
        # return True or False
        ship_type = msg[1]
        if not check_ship(ship_type):
            return False
        else:
            global type_of_ship
            type_of_ship = msg[1]
            global ship_count
            ship_count -= 1
            return True

    if msg[0] == 'ship_coord_msg':
        # return True or False
        msg_tup = msg[1]
        x, y, rotation = msg_tup[0], msg_tup[1], msg_tup[2]
        x = int(x)
        y = int(x)
        rotation = int(rotation)
        if not check_cell(type_of_ship, x, y, rotation):
            return False
        else:
            place_ship(type_of_ship, x, y, rotation)
            return True
