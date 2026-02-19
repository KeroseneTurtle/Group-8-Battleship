"""
battleship.py
The classic board game battleship
Erin, Aniel, and Malik
"""

import random
import os

row_names: list[str] = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
board_size: int = 10

# Define ship names
ship_ID: dict[int, str] = {0: "Empty",
                           1: "Destroyer",
                           2: "Submarine",
                           3: "Cruiser",
                           4: "Battleship",
                           5: "Carrier"}

ship_length: dict[int, int] = {1: 2, # Destroyer
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

player_board: dict[str, object] = make_empty_board()
computer_board: dict[str, object] = make_empty_board()

# info is called by board_name[row][column - 1][data_type]
# data_type: 0 calls shot fired, 1 calls ship ID
# ex. player_board["A"][(1) - 1][1] calls the ship ID stored in A1

## Draw Functions
# Clear screen
def clear_screen():
  os.system("cls" if os.name == "nt" else "clear")

# Board Printer Function
def draw_single_board(board: dict[str, object], show_ships: bool):
  print("    1   2   3   4   5   6   7   8   9   10 ")
  print("  -----------------------------------------")
  
  for row in row_names:
    print(f"{row} ", end="")
    for col in range(board_size):
      print("| ", end="")
      
      shot_fired: bool = board[row][col][0] # pyright: ignore[reportIndexIssue]
      ship: int  = board[row][col][1] # pyright: ignore[reportIndexIssue]
      if shot_fired:
        if ship != 0:
          print("X ", end="")  # hit
        else:
          print("O ", end="")  # miss
      else:
        if show_ships and ship != 0:
          print(f"{ship} ", end="")
        else:
          print("  ", end="")
    
    print("|")
    print("  -----------------------------------------")

def draw_board(player_board: dict[str, object], computer_board: dict[str, object]):
  print("\nShots you've taken:")
  draw_single_board(computer_board, show_ships=False)

  print("\nYour board:")
  draw_single_board(player_board, show_ships=True)

def show_coordinate_help():
    print("\nWelcome to Battleship!")
    print("Coordinates: Row(A-J) + Column(1-10)")
    print("Examples: B7, A1, J10")
    print("Ship placement: give START and END (same row or column)")
    print("Example: A1 A5 or A1 E1\n")

def show_board_legend():
  print("\nLegend:")
  print("X = Hit")
  print("O = Miss")
  print("Numbers = Your Ships")

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

    return (row_letter, col_num - 1)


# ask the user for a shot until they give a valid coordinate
def get_player_shot():
    while True:
        move = input("Enter shot (example B7): ")
        pos = parse_coord(move)

        if pos is not None:
            return pos

        print("Invalid coordinate. Try again.")

# Prompt the player to place a ship of given length.
def place_ship(board: dict[str, object], length: int):
  """
  Ensures:
    - Coordinates are valid
    - Ship is straight (horizontal or vertical)
    - Ship length matches the required length
    - Ship does not overlap existing ships
  Returns a list of (row, col) tuples for placement.
  """
  while True:
    clear_screen()
    print(f"Placing ship of length {length}")
    draw_single_board(board, show_ships=True)

    raw = input(f"Type START and END coordinates (example A1 A5): ").strip()
    parts = raw.split()
    if len(parts) != 2:
      print("Invalid input. You must enter exactly two coordinates.\n")
      continue

    start = parse_coord(parts[0])
    end = parse_coord(parts[1])
    if start is None or end is None:
      print("Invalid coordinates. Use format like A1 A5.\n")
      continue

    r1, c1 = start
    r2, c2 = end
    coords: list[tuple[str, int]] = []

    # Horizontal placement
    if r1 == r2:
      step = 1 if c2 >= c1 else -1
      coords = [(r1, c) for c in range(c1, c2 + step, step)]

    # Vertical placement
    elif c1 == c2:
      r1_idx = row_names.index(r1)
      r2_idx = row_names.index(r2)
      step = 1 if r2_idx >= r1_idx else -1
      coords = [(row_names[r], c1) for r in range(r1_idx, r2_idx + step, step)]

    else:
      print("Ships must be straight (horizontal or vertical).\n")
      continue

    if len(coords) != length:
      print(f"Ship must be exactly length {length}.\n")
      continue

    for r, c in coords:
      if any(board[r][c][1] != 0): # pyright: ignore[reportIndexIssue]
        print("That ship overlaps another one. Try again.\n")
        continue

    # Valid placement
    return coords

def place_ships_player(board: dict[str, object]):
  """
  Let the player place all ships on their board.
  Shows the board before each placement.
  """
  for ship_id, length in ship_length.items():
    while True:
      print("\nYour Fleet")
      print("=" * 42)
      draw_single_board(board, show_ships=True)
      print(f"Placing {ship_ID[ship_id]} (length {length})")

      coords = place_ship(board, length)

      # Place ship on the board
      for r, c in coords:
        board[r][c][1] = ship_id # pyright: ignore[reportIndexIssue]

      clear_screen()
      print(f"{ship_ID[ship_id]} placed successfully!\n")
      draw_single_board(board, show_ships=True)
      input("Press Enter to continue to next ship...")
      break



def place_ships_ai(board: dict[str, object]): # Erin contributed this one
  for ship_id, length in ship_length.items():
    placed = False

    while not placed:
      horizontal = random.choice([True, False])

      if horizontal:
        row = random.choice(row_names)
        col = random.randint(0, board_size - length)
        coords = [(row, col + i) for i in range(length)]
      else:
        col = random.randint(0, board_size - 1)
        start_row = random.randint(0, board_size - length)
        coords = [(row_names[start_row + i], col) for i in range(length)]

      # check overlap
      for r, c in coords:
        if all(board[r][c][1]) == 0: # pyright: ignore[reportIndexIssue]
          board[r][c][1] = ship_id # pyright: ignore[reportIndexIssue]
          placed = True

#===============================================================================
# Malik's stuff
def fire_shot(target_board: dict[str, object], row: str, col: int):
  # Check if player has previously targeted the cell
  if target_board[row][col][0] == True: # pyright: ignore[reportIndexIssue]
    return "already shot"
  
  # Set shot_fired to True
  target_board[row][col][0] = True # pyright: ignore[reportIndexIssue]
  
  if target_board[row][col][1] != 0: # pyright: ignore[reportIndexIssue]
    return "hit"
  else:
    return "miss"


def check_sunk(target_board: dict[str, object], ship_id: int):
  for row in row_names:
    for col in range(board_size):
      if target_board[row][col][1] == ship_id: # pyright: ignore[reportIndexIssue]
        if target_board[row][col][0] == False: # pyright: ignore[reportIndexIssue]
          return False  # found a part that hasnt been hit
  return True


def check_winner(target_board: dict[str, object]):
    for row in row_names:
        for col in range(board_size):
            if target_board[row][col][1] != 0: # pyright: ignore[reportIndexIssue]
                if target_board[row][col][0] == False: # pyright: ignore[reportIndexIssue]
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


## Core Gameplay Loop
def play_game():
  # Erin's UI Functions
  show_coordinate_help()
  show_board_legend()

  # Ship placements
  place_ships_player(player_board)
  place_ships_ai(computer_board)

  # Initialize shot tracker for computer opponent
  opponent_shots_fired: list[object] = []

  while True:
    draw_board(player_board, computer_board)  # Erin's function

    ## Player Turn
    # Get shot position from player
    print("YOUR TURN")
    player_shot_row, player_shot_col = get_player_shot()   # Aniel's function

    # Process player's decision and return feedback
    result = fire_shot(computer_board, player_shot_row, player_shot_col)
    if result == "already shot":
      print("You already shot there. Try again.")
      continue
    elif result == "hit":
      ship_id: int = computer_board[player_shot_row][player_shot_col][1] # pyright: ignore[reportIndexIssue]
      ship_name = ship_ID[ship_id]
      print(f"HIT! You hit their {ship_name}!")
      if check_sunk(computer_board, ship_id):
        print(f"You sunk their {ship_name}!")
    else:
      print(f"You missed at {player_shot_row}{str(player_shot_col + 1)}")

    # Check if player fired the winning shot
    if check_winner(computer_board) == True:
      draw_board(player_board, computer_board)
      print("YOU WIN!")
      break


    ## AI Turn
    print("\nOpponent is thinking...")
    ai_row, ai_col = ai_pick_shot(opponent_shots_fired)
    opponent_shots_fired.append((ai_row, ai_col))
    ai_result = fire_shot(player_board, ai_row, ai_col)

    # Check if the AI hit
    if ai_result == "hit":
      player_ship_hit: int = player_board[ai_row][ai_col][1] # pyright: ignore[reportIndexIssue]
      ship_hit_name = ship_ID[player_ship_hit]
      print(f"Opponent hit your {ship_hit_name} at {ai_row}{ai_col + 1}!")
      if check_sunk(player_board, player_ship_hit) == True: # pyright: ignore[reportIndexIssue]
        print(f"Opponent sunk your {ship_hit_name}.")
    else:
      print(f"Opponent missed at {ai_row}{ai_col + 1}")

    # Check if AI fired the winning shot
    if check_winner(player_board) == True:
      draw_board(player_board, computer_board)
      print("Game over. AI wins.")
      break

## Start the whole game
play_game()

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
