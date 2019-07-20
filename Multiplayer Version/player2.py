import socket
import select
import sys
from colorama import Fore, Back, Style
import pickle


client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
'''
We use socket.gethostname() because it will connect to a server on the same computer and machine so the host name is the same,
but usuqlly if we wanted the client to be remote and have them connect to a separate machine and another computer as the server
, we would put in a local or public IP often times
'''

# this example is how we handle inputs bigger than the buffer size, and it repeatedly accepts the message as a cycle

'''
a header is how our program knows how long the message is gonna be, and it's like ok once I have a message that size of 25, BOOM, that's how I know that message is done,
so now, I'm going to be waiting for another message again that is at most the size of the header, and once we reach that size, then boom that message is done, and we are now
onto the new message, and etc. the cycle repeats
'''
'''
# Print out usage statement, if the user has provided commandline arguments
if len(sys.argv) != 3:
    print 'usage:', sys.argv[0], '<server IP> <port>'
    sys.exit(0)


# Gather the HOST IP and PORT number from commandline arguments
HOST = sys.argv[1]
PORT = int(sys.argv[2])
'''

client_sock.connect((socket.gethostname(), 5555))

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

def is_board_full(board, possible_winner):
    if possible_winner == None:
        sum = 0
        for i in range(0, len(board)):
            for j in range(0, len(board[0])):
                if board[i][j] == u"\u001b[36mX" or board[i][j] == u"\u001b[33mO":
                    sum += 1
        if sum == len(board) * len(board[0]):
            return True

print("Welcome to Tic-Tac-Toe. The rules are the same, and you can type ''exit'' if you want to forfeit.")
render([[None, None, None], [None, None, None], [None, None, None]])
player2Name = input("Player 2 (O), Enter in your name: ")
client_sock.send(player2Name.encode())
player1Name = client_sock.recv(2048).decode()

i = 1
board = [[None, None, None], [None, None, None], [None, None, None]]
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
    if i % 2 == 1:
        recv_board = client_sock.recv(2048)
        board = pickle.loads(recv_board)
        print(board)
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
        render(board)
    else:
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
        updated_board = pickle.dumps(board)
        client_sock.send(updated_board)
    i += 1


client_sock.close()
