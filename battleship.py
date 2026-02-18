"""
battleship.py
The classic board game battleship
Erin, Aniel, and Malik
"""

import random

row_names: list[str] = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
board_size = 10

# Define ship names
ship_ID = {0: "Empty",
           1: "Destroyer",
           2: "Submarine",
           3: "Cruiser",
           4: "Battleship",
           5: "Carrier"}

ship_length = {1: 2, # Destroyer
               2: 3, # Submarine
               3: 3, # Cruiser
               4: 4, # Battleship
               5: 5} # Carrier

## Create empty board
# New boards will be made as copies of this empty board
# Each square of the grid keeps track of both shot status and ship ID
# They are stored in the form [shot fired, ship ID]

def make_empty_board():
    board: dict[str, object] = {}
    for row in row_names:
        board[row] = [[False, 0] for _ in range(10)]
    return board

player_board = make_empty_board()
computer_board = make_empty_board()

# info is called by board_name[row][column - 1][data_type]
# data_type: 0 calls shot fired, 1 calls ship ID
# ex. player_board["A"][(1) - 1][1] calls the ship ID stored in A1

## Computer Board Printer Function
print("Shots you've taken:")
print("    1   2   3   4   5   6   7   8   9   10 ")
print("  -----------------------------------------")
for row in row_names:
  print(f"{row} ",end="")
  for column in range(10):
     print("| ",end="")
     if computer_board[row][column][0] == True: # type: ignore
        if computer_board[row][column][1] != 0: # type: ignore
           print("X ",end="")
        else:
           print("O ",end="")
     else: 
        print("  ",end="")
  print("|")
  print("  -----------------------------------------")

print("")

## Player Board Printer Function
print("Your board:")
print("    1   2   3   4   5   6   7   8   9   10 ")
print("  -----------------------------------------")
for row in row_names:
  print(f"{row} ",end="")
  for column in range(10):
     print("| ",end="")
     if player_board[row][column][0] == True: # type: ignore
        if player_board[row][column][1] != 0: # type: ignore
           print("X ",end="")
        else:
           print("O ",end="")
     elif player_board[row][column][1] != 0:             # type: ignore
        print(f"{player_board[row][column][1]} ",end="") # type: ignore
     else: 
        print("  ",end="")
  print("|")
  print("  -----------------------------------------")

# ==============================================================================

# Aniel's stuff
# turn user input like B7 into row and column numbers
def parse_coord(text: str):
    text = text.strip().upper()

    if len(text) < 2:
        return None

    row_letter = text[0]
    if row_letter not in row_names:
        return None

    try:
        col_num = int(text[1:])
    except:
        return None

    if col_num < 1 or col_num > board_size:
        return None

    row = row_letter
    col = col_num
    return (row, col)


# ask the user for a shot until they give a valid coordinate
def get_player_shot():
    while True:
        move = input("Enter shot (example B7): ")
        pos = parse_coord(move)

        if pos is not None:
            return pos

        print("Invalid coordinate. Try again.")


# ask the user to place a ship and return the coordinates
def place_ship(length: int):
    while True:
        raw = input("Place ship length " + str(length) + " (example A1 A5): ")
        parts = raw.split()

        if len(parts) != 2:
            print("Type two coordinates.")
            continue

        start = parse_coord(parts[0])
        end = parse_coord(parts[1])

        if start is None or end is None:
            print("Invalid coordinates.")
            continue

        r1, c1 = start
        r2, c2 = end

        coords = []

        # horizontal ship
        if r1 == r2:
            step = 1 if c2 >= c1 else -1
            c = c1
            while c != c2 + step:
                coords.append((r1, c))
                c += step

        # vertical ship
        elif c1 == c2:
            step = 1 if r2 >= r1 else -1
            r = r1
            while r != r2 + step:
                coords.append((r, c1))
                r += step

        else:
            print("Ship must be straight.")
            continue

        if len(coords) != length:
            print("Ship must be length", length)
            continue

        return coords




print(place_ship(4))

# ==============================================================================

# maliks stuff below
def fire_shot(target_board, row, col):
    # already shot here?
    if target_board[row][col][0] == True:
        return "already shot"
    
    target_board[row][col][0] = True
    
    if target_board[row][col][1] != 0:
        return "hit"
    else:
        return "miss"


def check_sunk(target_board, ship_id):
    for row in row_names:
        for col in range(board_size):
            if target_board[row][col][1] == ship_id:
                if target_board[row][col][0] == False:
                    return False  # found a part that hasnt been hit
    return True


def check_winner(target_board):
    for row in row_names:
        for col in range(board_size):
            if target_board[row][col][1] != 0:
                if target_board[row][col][0] == False:
                    return False
    return True


# ai is just random for now
# to do next submission we make it smarter and stuff

def ai_pick_shot(ai_shots_fired):
    untried = []
    for row in row_names:
        for col in range(board_size):
            coordinate = (row, col)
            if coordinate not in ai_shots_fired:
                untried.append(coordinate)
    pick = random.choice(untried)
    return pick


# def play_game():
#   place_ships(player_board)   # somebodys elses
#   place_ships(computer_board)

#   ai_shots_fired = []

#   while True:
#       draw_board(player_board, computer_board)  # erin's setting that up

#       # players turn to shoot at the ai
#       print("YOUR TURN")
#       row, col = get_player_shot()   # aniel's function
#       result = fire_shot(computer_board, row, col)

#       if result == "already shot":
#         print("you already shot there try again")
#         ontinue
#       elif result == "hit":
#         ship_id = computer_board[row][col][1]
#         ship_name = ""
#         for name, sid, length in ships:
#           if sid == ship_id:
#             ship_name = name
#             break
#             print("HIT!! you hit their " + ship_name + "!")
#             if check_sunk(computer_board, ship_id) == True:
#                 print("you sunk their " + ship_name + "!!")
#         else:
#             print("miss :( " + row + str(col + 1))

#         if check_winner(computer_board) == True:
#             draw_board(player_board, computer_board)
#             print("YOU WIN!!!")
#             break

#         # this is the ais turn and stuff
#         print("\noppenent is thinking...")
#         ai_row, ai_col = ai_pick_shot(ai_shots_fired)
#         ai_shots_fired.append((ai_row, ai_col))
#         ai_result = fire_shot(player_board, ai_row, ai_col)

#         if ai_result == "hit":
#             ship_id = player_board[ai_row][ai_col][1]
#             ship_name = ""
#             for name, sid, length in ships:
#                 if sid == ship_id:
#                     ship_name = name
#             print("ai hit your " + ship_name + " at " + ai_row + str(ai_col + 1) + "!")
#             if check_sunk(player_board, ship_id) == True:
#                 print("ai sunk your " + ship_name + "...")
#         else:
#             print("oppenent missed at ", ai_row, str(ai_col + 1))

#         if check_winner(player_board) == True:
#             draw_board(player_board, ai_board)
#             print("game over :( ai wins")
#             break


# play_game()




## User interface design
""" Shots tracking board (upper board)
    1   2   3   4   5   6   7   8   9   10
  -----------------------------------------
A |   |   | O |   |   |   |   |   |   |   |
  -----------------------------------------
B |   |   |   |   |   | O |   |   |   | O |
  -----------------------------------------
C |   |   |   |   |   |   |   |   |   |   |
  -----------------------------------------
D | X |   |   |   |   |   | X | X | X |   |
  -----------------------------------------
E |   |   |   |   |   |   |   |   | O |   |
  -----------------------------------------
F |   | O |   |   |   |   |   |   |   |   |
  -----------------------------------------
G |   |   |   |   |   |   |   |   |   |   |
  -----------------------------------------
H | O |   |   |   | X |   |   |   | X | X |
  -----------------------------------------
I |   | O |   |   | X |   |   | O |   |   |
  -----------------------------------------
J |   |   |   |   | X |   |   |   |   |   |
  -----------------------------------------
  
  Player board (lower board)
    1   2   3   4   5   6   7   8   9   10
  -----------------------------------------
A |   |   | O |   |   |   |   |   |   |   |
  -----------------------------------------
B | 1 | X |   |   |   |   |   | 4 |   |   |
  -----------------------------------------
C |   |   |   |   | O |   |   | X |   |   |
  -----------------------------------------
D |   |   |   |   |   |   |   | 4 |   |   |
  -----------------------------------------
E |   |   |   |   |   |   |   | 4 |   | 3 |
  -----------------------------------------
F | 5 | X | X | 5 | X |   |   |   |   | 3 |
  -----------------------------------------
G | O |   |   |   |   |   |   | O |   | 3 |
  -----------------------------------------
H |   |   |   |   |   |   |   |   |   |   |
  -----------------------------------------
I |   |   |   | 2 | 2 | 2 |   |   |   | O |
  -----------------------------------------
J |   |   | O |   |   |   |   |   |   |   |
  -----------------------------------------
"""
