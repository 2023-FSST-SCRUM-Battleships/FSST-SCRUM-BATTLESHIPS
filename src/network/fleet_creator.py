# contains types of ship - their name, form and how many of them are available
ship_types = [
    {
        "name": "Carrier",
        "form": [[0, 0], [1, 0], [2, 0], [1, 1], [2, 1], [3, 1]],
        "count": 1
    },
    {
        "name": "Submarine",
        "form": [[0, 0], [1, 0], [2, 0]],
        "count": 2
    },
    {
        "name": "Destroyer",
        "form": [[0, 0], [1, 0]],
        "count": 3
    }
]

rotation_map = [
    lambda x, y: (x, y),
    lambda x, y: (y, x),
    lambda x, y: (-x, -y),
    lambda x, y: (-y, -x),
]

# every ship in the grid will be shown with a different number
ship_index = 0
# the total number of ships available
ship_count = 3
# list that saves the coordinates of each hit as a tuple
list_of_hits = []
# list where the coordinates of each created ship (["form"]) are saved
my_fleet = []
# number of hits
hits = 5


def create_board(size: int):
    """
    This function creates a 2d list for the board's grid
    :param size:
    :return 2d list 12x12:
    """
    return [[" " for x in range(size)] for y in range(size)]


def print_board(brd: list[list]):
    """
    This function prints the board
    :param brd: return value of the create_board function
    :return:
    """
    print("  | 01| 02| 03| 04| 05| 06| 07| 08| 09| 10| 11| 12|")
    print("--+---+---+---+---+---+---+---+---+---+---+---+---+")

    for y in range(len(brd)):
        accu = f"{y + 1:02}"
        for x in range(len(brd[y])):
            accu += f"| {brd[y][x]} "
        print(accu + "|")
        print("--+---+---+---+---+---+---+---+---+---+---+---+---+")


# creating a list for the coordinates of my board
my_board = create_board(12)
print_board(my_board)

# creating a list for the board-coordinates of the opponents board
opponent_board = create_board(12)


def ship_input():
    """
    This function gets the user input - which ship type a user wants to place
    :param:
    :return: dictionary
    """
    input_ship = int(input("Which ship would you like to place?"))
    # gets the dictionary with values: name, form and count from the ship_types list based on the type of ship
    ship_type = ship_types[input_ship]
    return ship_type


def coord_input():
    """
    This function gets the user input - where the ship should be placed and how
    :param:
    :return: x, y coordinate and rotation
    """
    input_cell = input("Where would you like to place the ship? ")
    x, y, rotation = (int(bit) for bit in input_cell.split(" "))
    x, y = x - 1, y - 1
    return x, y, rotation


def place_ship(ship_type: dict, x: int, y: int, rotation: int):
    """
    This function is used to place the ship
    :param: ship_t, x, y, rotation
    :return:
    """
    global ship_index
    ship_index += 1
    # list that saves each coordinate as a tuple in a list = [(y, x), (y, x)...]
    my_ship = []
    # ship_type = int(ship_type)
    for coord in ship_type["form"]:
        relX, relY = (i for i in coord)
        relX, relY = rotation_map[rotation](relX, relY)
        # gives the name to each coordinate
        my_board[y + relY][x + relX] = ship_index
        my_ship.append((y + relY, x + relX))
    # saves the whole ship in a my_fleet list
    my_fleet.append(my_ship)


def check_ship(ship_type):
    """
    This function check if any ship of the chosen type is available
    :param: ship_type
    :return: bool
    """
    # ship_type = int(ship_type)
    if ship_type["count"] > 0:
        ship_type["count"] -= 1
        return True
    else:
        print("You already used all ships od this type!")
        return False


def check_cell(ship_type: dict, x: int, y: int, rotation: int):
    """
    This function checks if the input-coordinates (and the following ones defined in ['form'])
    where the ship should be placed are free
    :param: ship_type, x, y coordinate and rotation
    :return: bool
    """
    global my_board
    count = 0
    # ship_type = int(ship_type)
    for coord in ship_type["form"]:
        relX, relY = (i for i in coord)
        relX, relY = rotation_map[rotation](relX, relY)
        if my_board[y + relY][x + relX] == ' ':
            count += 1
    # if all cells are free return True
    if count == len(ship_type["form"]):
        return True
    else:
        print("You already placed some ship here!")
        return False


def creating_fleet():
    """
    This function creates the fleet and handles invalid input
    :param:
    :return:
    """
    try:
        ship_type = ship_input()
        while not check_ship(ship_type):
            ship_type = ship_input()

        global ship_count
        ship_count -= 1
        x, y, rotation = coord_input()
        while not check_cell(ship_type, x, y, rotation):
            x, y, rotation = coord_input()
        place_ship(ship_type, x, y, rotation)
        print_board(my_board)
    except ValueError:
        print("Enter a valid input!")


# creating a fleet
while ship_count > 0:
    creating_fleet()

print(my_fleet)


def get_ship_name(list_len: int):
    """
    This function gets the name of the ship that has been sunk
    :param: length of the list which represents coordinates of a ship and is saved in my_fleet list
    :return: str
    """
    if list_len == 6:
        return ship_types[0]["name"]
    if list_len == 3:
        return ship_types[1]["name"]
    if list_len == 2:
        return ship_types[0]["name"]


def check_list_contains_all_elements(list1: list, list2: list):
    """
    This function checks if all elements of a first list are  contained in the second list
    :param: list1 - coordinates of the ship | list2 - list of hits
    :return: bool
    """
    return all(element in list2 for element in list1)


def check_if_sunk(hit_coord: tuple):
    """
    This function checks if a ship has been sunk
    :param: coordinates x, y of a hit
    :return: tuple containing a bool indicating if a ship was sunk and the name of the ship that was hit
    """
    for ship in my_fleet:
        for coord in ship:
            if coord == hit_coord:
                if check_list_contains_all_elements(ship, list_of_hits):
                    ship_hit = get_ship_name(len(ship))
                    return True, ship_hit
    return False, ""


def hit_ship():
    """
    This function gets the coordinates for the hit, checks if hit or missed and if sunk
    :param: coordinates x, y of a hit
    :return:
    """
    input_cell = input("Give a coordinate that you want to hit:")
    x, y = (int(bit) - 1 for bit in input_cell.split(" "))
    if my_board[x][y] == " ":
        print("Oh no, You missed it! Try again!")
        opponent_board[x][y] = "X"
    else:
        print("You hit a ship!")
        list_of_hits.append((x, y))
        opponent_board[x][y] = "$"
        is_sunk, ship_hit = check_if_sunk((x, y))
        if is_sunk:
            print(f"You sunk a {ship_hit}!")
        else:
            print("None ship is sunk! Continue to hit!")


'''while hits > 0:
    hit_ship()
    print("OPPONENTS BOARD")
    print_board(opponent_board)'''
