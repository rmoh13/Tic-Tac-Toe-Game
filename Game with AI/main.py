import sys
import random
from math import *
from colorama import Fore, Back, Style

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
        turn = u"\u001b[36mX"
    else:
        turn = u"\u001b[33mO"
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
                if board[i][j] == u"\u001b[36mX" or board[i][j] == u"\u001b[33mO":
                    sum += 1
        if sum == len(board) * len(board[0]):
            return True

def random_AI(board, current_player):
    coord_options = []
    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == " ":
                coord_options.append((i,j))
    coords = random.choice(coord_options)
    return coords
'''
board = [
  ['X', 'O', None],
  ['O', 'O', None],
  ['X', None, None]
]
print(random_AI(board))
'''

def finds_winning_moves_AI(board, turn):
    if turn % 2 == 1:
        current_player = u"\u001b[36mX"
    else:
        current_player = u"\u001b[33mO"
    winning_spot = False
    list_all_lines = []
    list_all_lines_coords = []
    list_all_lines_coords.append([(0,0), (1,0), (2,0)])
    list_all_lines_coords.append([(0,1), (1,1), (2,1)])
    list_all_lines_coords.append([(0,2), (1,2), (2,2)])
    [list_all_lines.append(i) for i in board]

    diag1 = []
    diag1.append(board[0][0])
    diag1.append(board[1][1])
    diag1.append(board[2][2])
    list_all_lines.append(diag1)
    list_all_lines_coords.append([(0,0), (1,1), (2,2)])
    diag2 = []
    diag2.append(board[0][2])
    diag2.append(board[1][1])
    diag2.append(board[2][0])
    list_all_lines.append(diag2)
    list_all_lines_coords.append([(2,0), (1,1), (0,2)])

    for i in range(0, len(board[0])):
        col = []
        col_coord = []
        for j in range(0, len(board)):
            col.append(board[j][i])
            col_coord.append((i,j))
        list_all_lines.append(col)
        list_all_lines_coords.append(col_coord)
    #print(list_all_lines)
    for i in range(0, len(list_all_lines_coords)):
        # sets must have distinct elements
        similarity_counter = 0
        for j in range(0, len(list_all_lines_coords[0])):
            if board[list_all_lines_coords[i][j][0]][list_all_lines_coords[i][j][1]] == current_player:
                similarity_counter += 1
        if similarity_counter == 2:
            for j in range(0, len(list_all_lines_coords[0])):
                if board[list_all_lines_coords[i][j][0]][list_all_lines_coords[i][j][1]] == " ":
                    winning_spot = list_all_lines_coords[i][j]
    if winning_spot == False:
        coords = random_AI(board, turn)
        return coords
    else:
        coords = winning_spot
        return coords
'''
board = [
  [u"\u001b[36mX", u"\u001b[33mO", " "],
  [" ", u"\u001b[33mO", " "],
  [u"\u001b[36mX", " ", " "]
]
print(finds_winning_moves_AI(board, 2))
'''

def finds_winning_and_losing_moves_AI(board, turn):
    if turn % 2 == 1:
        current_player = u"\u001b[36mX"
        opponent = u"\u001b[33mO"
    else:
        current_player = u"\u001b[33mO"
        opponent = u"\u001b[36mX"
    coord1 = finds_winning_moves_AI(board, turn)
    coord2 = finds_winning_moves_AI(board, turn + 1)
    coord3 = random_AI(board, turn)

def human_player(board, turn):
    x_coord = input("What is your move's X coordinate? ")
    y_coord = input("What is your move's Y coordinate? ")
    if "exit" in x_coord or "exit" in y_coord:
        print(Fore.RED + "Aww, you forfeited!")
        sys.exit()
    try:
        coords = (int(x_coord), int(y_coord))
    except ValueError:
        print("You didn't type in a number! Try again.")
        return False
    return coords

'''
The below code before run_game() is just to look at average win percentages for the different AIs pitted up against each other.
'''
def play(first_AI, second_AI):
    if "random" in first_AI and "slight" in second_AI:
        i = 1
        board = new_board()
        render(board)
        while True:
            if i % 2 == 1:
                winner = get_winner(board)
                if winner == u"\u001b[36mX":
                    print(Fore.GREEN + u"\u001b[36mRandom" + " wins the game!")
                    break
                elif winner == u"\u001b[33mO":
                    print(Fore.GREEN + u"\u001b[33mSlightly Intelligent AI" + " wins the game!")
                    break
                if is_board_full(board, winner):
                    print("It's a draw!")
                    break
                coords = random_AI(board, i)
                board = make_move(board, coords, i)
                render(board)
            else:
                winner = get_winner(board)
                if winner == u"\u001b[36mX":
                    print(Fore.GREEN + u"\u001b[36mX" + " wins the game!")
                    break
                elif winner == u"\u001b[33mO":
                    print(Fore.GREEN + u"\u001b[33mO" + " wins the game!")
                    break
                if is_board_full(board, winner):
                    print("It's a draw!")
                    break
                coords = finds_winning_moves_AI(board, i)
                board = make_move(board, coords, i)
                render(board)
            i += 1

        if winner == u"\u001b[36mX":
            return 1
        elif winner == u"\u001b[33mO":
            return 2
        else:
            return 0

def repeated_battle(N, first_AI, second_AI):
    sum = 0
    for i in range(0, N):
        sum += play(first_AI, second_AI)
    average = sum / N
    return average
#print(repeated_battle(50, "random", "slightly"))

# assume the AI is player 1 or 'X' and the opponent is player 2 or 'O' for simplicity. Remember K.I.S.S.
def minimax_score(board, turn):
    if turn % 2 == 1:
        current_player = u"\u001b[36mX"
        opponent = u"\u001b[33mO"
    else:
        current_player = u"\u001b[33mO"
        opponent = u"\u001b[36mX"

    winner = get_winner(board)
    if winner == u"\u001b[36mX":
        return 10
    elif winner == u"\u001b[33mO":
        return -10
    if is_board_full(board, winner):
        return 0

    available_moves = []
    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == " ":
                available_moves.append((i,j))

    if current_player == u"\u001b[36mX":
        # we wanna find the max
        best = -10000
        for i in range(0, len(available_moves)):
            temp_board = make_move(board, available_moves[i], turn)
            score = minimax_score(temp_board, turn+1)
            if score > best:
                best = score
    elif current_player == u"\u001b[33mO":
        # we wanna find the min
        best = 10000
        for i in range(0, len(available_moves)):
            temp_board = make_move(board, available_moves[i], turn)
            score = minimax_score(temp_board, turn+1)
            if score < best:
                best = score
    return best

def minimax_AI(board, turn):
    available_moves = []
    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == " ":
                available_moves.append((i,j))

    for i in range(0, len(available_moves)):
        temp_board = make_move(board, available_moves[i], turn)
        if minimax_score(temp_board, turn) >= 0:
            return available_moves[i]

def run_game():
    board = new_board()
    print(board)
    render(board)
    print("Welcome to Tic-Tac-Toe. The rules are the same, and you can type ''exit'' if you want to forfeit.")
    print("You can play against another person or an AI")
    option = input("Do you want to watch different AIs battle against each other OR play against another player, a slightly intelligent AI, a very intelligent AI, or a dumb AI making random moves? ")
    if 'watch' not in option:
        if 'player' in option:
            player1Name = input("Player 1 (X), Enter in your name: ")
            player2Name = input("Player 2 (O), Enter in your name: ")
            i = 1
            while True:
                winner = get_winner(board)
                if winner == u"\u001b[36mX":
                    print(Fore.GREEN + player1Name + " wins the game!")
                    break
                elif winner == u"\u001b[33mO":
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
        elif 'random' in option:
            i = 1
            while True:
                winner = get_winner(board)
                if winner == u"\u001b[36mX":
                    print(Fore.GREEN + u"\u001b[36mX" + " wins the game!")
                    break
                elif winner == u"\u001b[33mO":
                    print(Fore.GREEN + u"\u001b[33mO" + " wins the game!")
                    break
                if is_board_full(board, winner):
                    print("It's a draw!")
                    break
                coords = random_AI(board, i)
                board = make_move(board, coords, i)
                render(board)
                i += 1
        elif 'slight' in option:
            i = 1
            while True:
                winner = get_winner(board)
                if winner == u"\u001b[36mX":
                    print(Fore.GREEN + u"\u001b[36mX" + " wins the game!")
                    break
                elif winner == u"\u001b[33mO":
                    print(Fore.GREEN + u"\u001b[33mO" + " wins the game!")
                    break
                if is_board_full(board, winner):
                    print("It's a draw!")
                    break
                coords = finds_winning_moves_AI(board, i)
                board = make_move(board, coords, i)
                render(board)
                i += 1
        elif 'very' in option:
            i = 1
            while True:
                winner = get_winner(board)
                if winner == u"\u001b[36mX":
                    print(Fore.GREEN + u"\u001b[36mX" + " wins the game!")
                    break
                elif winner == u"\u001b[33mO":
                    print(Fore.GREEN + u"\u001b[33mO" + " wins the game!")
                    break
                if is_board_full(board, winner):
                    print("It's a draw!")
                    break
                coords = minimax_AI(board, i)
                board = make_move(board, coords, i)
                render(board)
                i += 1
    else:
        option2 = input("\nWhich AIs from the aforementioned list do you want to watch? The second player is the slightly intelligent by default.\nEnter here: ")
        if 'random' in option2:
            i = 1
            while True:
                if i % 2 == 1:
                    winner = get_winner(board)
                    if winner == u"\u001b[36mX":
                        print(Fore.GREEN + u"\u001b[36mX" + " wins the game!")
                        break
                    elif winner == u"\u001b[33mO":
                        print(Fore.GREEN + u"\u001b[33mO" + " wins the game!")
                        break
                    if is_board_full(board, winner):
                        print("It's a draw!")
                        break
                    coords = random_AI(board, i)
                    board = make_move(board, coords, i)
                    render(board)
                else:
                    winner = get_winner(board)
                    if winner == u"\u001b[36mX":
                        print(Fore.GREEN + u"\u001b[36mX" + " wins the game!")
                        break
                    elif winner == u"\u001b[33mO":
                        print(Fore.GREEN + u"\u001b[33mO" + " wins the game!")
                        break
                    if is_board_full(board, winner):
                        print("It's a draw!")
                        break
                    coords = finds_winning_moves_AI(board, i)
                    board = make_move(board, coords, i)
                    render(board)
                i += 1
        elif 'slight' in option2:
            i = 1
            while True:
                winner = get_winner(board)
                if winner == u"\u001b[36mX":
                    print(Fore.GREEN + u"\u001b[36mX" + " wins the game!")
                    break
                elif winner == u"\u001b[33mO":
                    print(Fore.GREEN + u"\u001b[33mO" + " wins the game!")
                    break
                if is_board_full(board, winner):
                    print("It's a draw!")
                    break
                coords = finds_winning_moves_AI(board, i)
                board = make_move(board, coords, i)
                render(board)
                i += 1

run_game()
