# Small pure-Python test for board expansion logic
import sys, os
# add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.constants import BOARD_EXPANSION_SIZE, MAX_BOARD_SIZE

def expand_board(board, add_top=0, add_bottom=0, add_left=0, add_right=0):
    old_h = len(board)
    old_w = len(board[0]) if old_h>0 else 0
    new_h = old_h + add_top + add_bottom
    new_w = old_w + add_left + add_right
    new_board = [[0 for _ in range(new_w)] for _ in range(new_h)]
    for i in range(old_h):
        for j in range(old_w):
            new_board[i + add_top][j + add_left] = board[i][j]
    return new_board

# create 5x5 board with marks on right side
board = [[0]*5 for _ in range(5)]
# mark rightmost column with O(2)
for i in range(5):
    board[i][4] = 2
# mark some in middle
board[2][2] = 1

print('Original board:')
for row in board:
    print(row)

# simulate expanding left by 2
new = expand_board(board, add_top=0, add_bottom=0, add_left=2, add_right=0)
print('\nAfter expand left by 2:')
for row in new:
    print(row)

# simulate expanding left by 2 and right by 0 using method like in code

# Also simulate expand top by 1 and left by 2
new2 = expand_board(board, add_top=1, add_bottom=0, add_left=2, add_right=0)
print('\nAfter expand top 1 left 2:')
for row in new2:
    print(row)
