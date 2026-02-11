"""
battleship.py
The classic board game battleship
Erin, Aniel, and Malik
"""
## Create empty board
# Each square of the matrix keeps track of both shot status and ship ID
# They are stored in the form [shot_fired, ship_ID]

# Define the row names as a list
row_names: list[str] = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

# Create a ten item long empty row of [shot_fired, ship_ID]
empty_row: list[object] = []
for column in range(len(row_names)):
    empty_row.append([False, 0])

# Create a dictionary entry for each row name and fill it with a blank row
empty_board: dict[str, object] = {}
for item in row_names:
    empty_board[item] = empty_row

## info is called by board["row"][column - 1][data_type] 
# data_type: 0 checks for a shot in the square, 1 checks for ship ID in the square
print(empty_board["A"][0][1])


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
