# types of ship
ship_types = [
    {
        "ship": 0,
        "form": [[0, 0], [1, 0], [2, 0], [1, 1], [2, 1], [3, 1]],
        "count": 1
    },
    {
        "ship": 1,
        "form": [[0, 0], [1, 0], [2, 0]],
        "count": 2
    },
    {
        "ship": 2,
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

ship_count = 6


def create_board(size):
    return [[" " for x in range(size)] for y in range(size)]


def print_board(board: list[list]):
    print("  | 01| 02| 03| 04| 05| 06| 07| 08| 09| 10| 11| 12|")
    print("--+---+---+---+---+---+---+---+---+---+---+---+---+")

    for y in range(len(board)):
        accu = f"{y + 1:02}"
        for x in range(len(board[y])):
            accu += f"| {board[y][x]} "
        print(accu + "|")
        print("--+---+---+---+---+---+---+---+---+---+---+---+---+")


board = create_board(12)
print_board(board)


def ship_input():
    input_ship = int(input("Which ship would you like to place?"))
    # gets the dictionary from the ship_types list based on the type of ship
    ship_type = ship_types[input_ship]
    return ship_type


def coord_input():
    input_cell = input("Where would you like to place the ship? ")
    x, y, rotation = (int(bit) for bit in input_cell.split(" "))
    x, y = x - 1, y - 1
    return x, y, rotation


def place_ship(ship_type, x, y, rotation):
    for coord in ship_type["form"]:
        relX, relY = (i for i in coord)
        relX, relY = rotation_map[rotation](relX, relY)
        board[y + relY][x + relX] = ship_type["ship"]


def check_ship(ship_type):
    # checks if there is any ship left
    if ship_type["count"] > 0:
        ship_type["count"] -= 1
        return True
    else:
        print("You already used all ships od this type!")
        return False


def check_cell(ship_type, x, y, rotation):
    global board
    count = 0
    for coord in ship_type["form"]:
        relX, relY = (i for i in coord)
        relX, relY = rotation_map[rotation](relX, relY)
        if board[y + relY][x + relX] == ' ':
            count += 1
    # if all cells are free return True
    if count == len(ship_type["form"]):
        return True
    else:
        print("You already placed some ship here!")
        return False


def fleet_creator():
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
        print_board(board)
    except ValueError:
        print("Enter a valid input!")


while ship_count > 0:
    fleet_creator()
