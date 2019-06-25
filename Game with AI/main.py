import sys

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
    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == 'X':
                board[i][j] = u"\u001b[36mX"
            elif board[i][j] == 'O':
                board[i][j] = u"\u001b[33mO"
    # this manual way is actually quicker and simpler than a complicated for loop with an if-else statement inside
    # we're formatting this a bit differently as x,y coordinates
    print(u"\u001b[37m0  " + board[0][0] + u"\u001b[37m | " + board[1][0] + u"\u001b[37m | " + board[2][0])
    line = [u"\u001b[37m_" for i in range(0, len(board[0])+8)]
    print("  " + "".join(line))
    print(u"\u001b[37m1  " + board[0][1] + u"\u001b[37m | " + board[1][1] + u"\u001b[37m | " + board[2][1])
    print("  " + "".join(line))
    print(u"\u001b[37m2  " + board[0][2] + u"\u001b[37m | " + board[1][2] + u"\u001b[37m | " + board[2][2])
#board = new_board()
#board[0][1] = 'X'
#board[1][1] = 'O'
#render(board)

def get_move(num, player1Name, player2Name):
    if num % 2 == 1:
        x_coord = input(player1Name + ": What is your move's X coordinate? ")
        y_coord = input(player1Name + ": What is your move's Y coordinate? ")
        if "exit" in x_coord or "exit" in y_coord:
            print(Fore.RED + "Aww, you forfeited! %s wins!" % player2Name)
            sys.exit()
    else:
        x_coord = input(player2Name + ": What is your move's X coordinate? ")
        y_coord = input(player2Name + ": What is your move's Y coordinate? ")
        if "exit" in x_coord or "exit" in y_coord:
            print(Fore.RED + "Aww, you forfeited! %s wins!" % player1Name)
            sys.exit()
    try:
        coords = (int(x_coord), int(y_coord))
    except ValueError:
        print("You didn't type in a number! Try again.")
        return False
    return coords
#print(get_move())

def make_move(board, coords, num):
    # we could update the given board or just return a new board, let's do the latter because it might be easier to work with
    if num % 2 == 1:
        turn = "X"
    else:
        turn = "O"
    new_board = board
    if coords[0] >= len(board) or coords[1] >= len(board[0]):
        print("Invalid move! Your choice is off the grid. Try again.")
        return False
    elif board[coords[0]][coords[1]] == " ":
        new_board[coords[0]][coords[1]] = turn
        return new_board
    else:
        print("Invalid move! That spot is already taken. Try again.")
        return False

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

def is_board_full(board, possible_winner):
    if possible_winner == None:
        sum = 0
        for i in range(0, len(board)):
            for j in range(0, len(board[0])):
                if board[i][j] == 'X' or board[i][j] == 'O':
                    sum += 1
        if sum == len(board) * len(board[0]):
            return True

def run_game():
    board = new_board()
    render(board)
    print("Welcome to Tic-Tac-Toe. The rules are the same, and you can type ''exit'' if you want to forfeit.")
    print("You can play against another person or an AI")
    option = input("Do you want to play against another player or an AI? ")
    player1Name = input("Player 1 (X), Enter in your name: ")
    player2Name = input("Player 2 (O), Enter in your name: ")
    if 'AI' not in option:
        i = 1
        while True:
            winner = get_winner(board)
            if winner == 'X':
                print(Fore.GREEN + player1Name + " wins the game!")
                break
            elif winner == 'O':
                print(Fore.GREEN + player2Name + " wins the game!")
                break
            if is_board_full(board, winner):
                print("It's a draw!")
                break
            coords = get_move(i, player1Name, player2Name)
            while coords == False:
                coords = get_move(i, player1Name, player2Name)
            b1 = board
            board = make_move(board, coords, i)
            while board == False:
                coords = get_move(i, player1Name, player2Name)
                while coords == False:
                    coords = get_move(i, player1Name, player2Name)
                board = make_move(b1, coords, i)
            render(board)
            i += 1
run_game()
