import socket
import select
import sys
from colorama import Fore, Back, Style
import pickle

'''
Use Python's pickle module to send objects. Here's the basics:
d = {1: "Hey", 2 : "There"}
msg = pickle.dumps(d) # this pickles it
print(msg) # this prints msg in bytes serialization format, so you don't even need to do encode or decode cause it's already a bytes object

on the other side
d = pickle.loads(msg)
print(d)
'''

# server = "" we just wanna use localhost meaning anyone on the same WiFi as me and connect to this server so look below
# server = "10.0.0.63"
port = 5555

# socket.AF_INET says that we create a socket complying with IPv4 Protocols and socket.SOCK_STREAM allows for a stream and represents how the server string comes in
"""
The first argument AF_INET is the address domain of the
socket. This is used when we have an Internet Domain with
any two hosts The second argument is the type of socket.
SOCK_STREAM means that data or characters are read in
a continuous flow.
"""
#server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
player1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
player1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#server_ip = socket.gethostbyname(server)

# bind our server and port to the newly created server socket
try:
    '''
    The IP Address of the server and the port address together is a complete address to a specific location on the computer (in this case it acts as a server)
    on which the server socket is opened as a node and endpoint of communication between the server and the client(s), and so that complete
    address is a tuple and our socket server binds to that
    '''
    #s.bind((server, port))
    player1.bind((socket.gethostname(), port))
except socket.error as e:
    print("Error or Exception:", str(e))

# our port is now opened and multiple clients can connect, but in our case we only want 1 client connecting at max at a time because this is player1
player1.listen(1)
print("Waiting for a connection, Server Started")
list_of_clients = []
player_names = []

player2, addr = player1.accept()
print("Connection by:", addr)


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

def run_game():
    player2Name = player2.recv(2048).decode()
    board = new_board()
    render(board)
    print("Welcome to Tic-Tac-Toe. The rules are the same, and you can type ''exit'' if you want to forfeit.")
    player1Name = input("Player 1 (X), Enter in your name: ")
    player2.send(player1Name.encode())
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
        if i >= 2 and i % 2 == 0:
            recv_board = player2.recv(2048)
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
        if i % 2 == 1:
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
            player2.send(updated_board)
        i += 1
        #player1.send(str(i).encode())

run_game()


server_socket.close()
