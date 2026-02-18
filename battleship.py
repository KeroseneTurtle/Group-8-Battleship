"""
battleship.py
The classic board game battleship
Erin, Aniel, and Malik
"""

# Define ship names/lengths and row names
ship_ID = {0: "Empty",
           1: "Destroyer",
           2: "Submarine",
           3: "Cruiser",
           4: "Battleship",
           5: "Carrier"}
ship_length = {1: 2, # destroyer
               2: 3, # submarine
               3: 3, # cruiser
               4: 4, # battleship
               5: 5} # carrier
row_names: list[str] = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

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
     if computer_board[row][column][0] == True:
        if computer_board[row][column][1] != 0:
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
     if player_board[row][column][0] == True:
        if player_board[row][column][1] != 0:
           print("X ",end="")
        else:
           print("O ",end="")
     elif player_board[row][column][1] != 0:
        print(f"{player_board[row][column][1]} ",end="")
     else: 
        print("  ",end="")
  print("|")
  print("  -----------------------------------------")
  
  

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
