
def new_board():
    #l = [[None] * 3] * 3 doesn't work because replicating a list with * doesn’t create copies, it only creates references to the existing objects, so it makes copies and you can't edit
    l = [None] * 3
    for i in range(0, len(l)):
        # you now generate 3 different lists
        l[i] = [None] * 3
    return l

def render(board):
    print("   0   1   2")
    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == None:
                board[i][j] = " "
    # this manual way is actually quicker and simpler than a complicated for loop with an if-else statement inside
    # we're formatting this a bit differently as x,y coordinates
    print("0  " + board[0][0] + " | " + board[1][0] + " | " + board[2][0])
    line = ["_" for i in range(0, len(board[0])+8)]
    print("  " + "".join(line))
    print("1  " + board[0][1] + " | " + board[1][1] + " | " + board[2][1])
    print("  " + "".join(line))
    print("2  " + board[0][2] + " | " + board[1][2] + " | " + board[2][2])
#board = new_board()
#board[0][1] = 'X'
#board[1][1] = 'O'
#render(board)

def get_move(i):
    if i % 2 == 1:
        x_coord = input("Player 1 (X): What is your move's X coordinate? ")
        y_coord = input("Player 1 (X): What is your move's Y coordinate? ")
    else:
        x_coord = input("Player 2 (O): What is your move's X coordinate? ")
        y_coord = input("Player 2 (O): What is your move's Y coordinate? ")
    coords = (int(x_coord), int(y_coord))
    return coords
#print(get_move())

def make_move(board, coords, turn):
    # we could update the given board or just return a new board, let's do the latter because it might be easier to work with
    new_board = board
    if board[coords[0]][coords[1]] == " ":
        new_board[coords[0]][coords[1]] = turn
        return new_board
    else:
        raise Exception("Invalid move!")

'''
board = new_board()
move_coords_1 = (2,0)
board = make_move(board, move_coords_1, 'X')
render(board)

move_coords_2 = (1,1)
board = make_move(board, move_coords_2, 'O')
render(board)
'''

'''
board = new_board()
move_coords = (2, 0)
board = make_move(board, move_coords, "X")
board = make_move(board, move_coords, "X")
render(board)
'''

'''
board = new_board()
move_coords = (2, 0)
move_coords2 = (2, 1)
board = make_move(board, move_coords, "X")
board = make_move(board, move_coords2, "X")
render(board)
'''

def get_winner(board):
    #list_all_lines = board doesn't work because it's still referencing board and is gonna change both board and list_all_lines, but we only wanna change list_all_lines as lists are mutable objects
    list_all_lines = []
    [list_all_lines.append(i) for i in board]
    diag1 = []
    diag1.append(board[0][0])
    diag1.append(board[1][1])
    diag1.append(board[2][2])
    list_all_lines.append(diag1)
    diag2 = []
    diag2.append(board[0][2])
    diag2.append(board[1][1])
    diag2.append(board[2][0])
    list_all_lines.append(diag2)

    for i in range(0, len(board[0])):
        col = []
        for j in range(0, len(board)):
            col.append(board[j][i])
        list_all_lines.append(col)
    #print(list_all_lines)
    winner = None
    for i in range(0, len(list_all_lines)):
        # sets must have distinct elements
        if type(list_all_lines[i][0]) == str and len(set(list_all_lines[i])) == 1:
            winner = list_all_lines[i][0]
    return winner

'''
board_1 = [
  ['X', 'X', 'O'],
  ['O', 'X', None],
  ['O', 'O', 'X'],
]
print(get_winner(board_1))
board_2 = [
  ['X', 'X', 'O'],
  ['O', None, 'X'],
  ['O', 'O', 'X'],
]
print(get_winner(board_2))
'''

def run_game():
    board = new_board()
    render(board)
    i = 1
    while True:
        winner = get_winner(board)
        if winner == 'X' or winner == 'O':
            print(winner + " wins the game!")
            break
        current_player = "X"
        if i % 2 == 1:
            current_player = "X"
        else:
            current_player = "O"
        coords = get_move(i)
        board = make_move(board, coords, current_player)
        render(board)
        i += 1
run_game()
