# Python program to implement server side of chat room.
import socket
import select
import sys
from _thread import *
from colorama import Fore, Back, Style

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
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# server_ip = socket.gethostbyname(server)

# bind our server and port to the newly created server socket
try:
    '''
    The IP Address of the server and the port address together is a complete address to a specific location on the computer (in this case it acts as a server)
    on which the server socket is opened as a node and endpoint of communication between the server and the client(s), and so that complete
    address is a tuple and our socket server binds to that
    '''
    #s.bind((server, port))
    server_socket.bind((socket.gethostname(), port))
except socket.error as e:
    print("Error or Exception:", str(e))

# our port is now opened and multiple clients can connect, but in our case we only want 2 clients connecting at max at a time
server_socket.listen(2)
print("Waiting for a connection, Server Started")
list_of_clients = []
player_names = []

def new_board():
    #l = [[None] * 3] * 3 doesn't work because replicating a list with * doesn’t create copies, it only creates references to the existing objects, so it makes copies and you can't edit
    l = [None] * 3
    for i in range(0, len(l)):
        # you now generate 3 different lists
        l[i] = [None] * 3
    return l

def renderListString(board):
    # this is basically useful for when we want to send this data to the server
    firstLine = "   0   1   2"
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
    secondLine = u"\u001b[37m0  " + board[0][0] + u"\u001b[37m | " + board[1][0] + u"\u001b[37m | " + board[2][0]
    line = [u"\u001b[37m_" for i in range(0, len(board[0])+8)]
    thirdLine = "  " + "".join(line)
    fourthLine = u"\u001b[37m1  " + board[0][1] + u"\u001b[37m | " + board[1][1] + u"\u001b[37m | " + board[2][1]
    fifthLine = "  " + "".join(line)
    sixthLine = u"\u001b[37m2  " + board[0][2] + u"\u001b[37m | " + board[1][2] + u"\u001b[37m | " + board[2][2]
    finalListofStrings = [firstLine, secondLine, thirdLine, fourthLine, fifthLine, sixthLine]
    return finalListofStrings

def make_move(board, coords, num, player1conn, player2conn):
    # we could update the given board or just return a new board, let's do the latter because it might be easier to work with
    if num % 2 == 1:
        turn = "X"
    else:
        turn = "O"
    new_board = board
    if coords[0] >= len(board) or coords[1] >= len(board[0]):
        if num % 2 == 1:
            player1conn.send(("Invalid move! Your choice is off the grid. Try again.").encode())
        else:
            player2conn.send(("Invalid move! Your choice is off the grid. Try again.").encode())
        return False
    elif board[coords[0]][coords[1]] == " ":
        new_board[coords[0]][coords[1]] = turn
        if num % 2 == 1:
            player1conn.send(("Valid Move!").encode())
        else:
            player2conn.send(("Valid Move!").encode())
        return new_board
    else:
        if num % 2 == 1:
            player1conn.send(("Invalid move! That spot is already taken. Try again.").encode())
        else:
            player2conn.send(("Invalid move! That spot is already taken. Try again.").encode())
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
                if board[i][j] == 'X' or board[i][j] == 'O':
                    sum += 1
        if sum == len(board) * len(board[0]):
            return True

board = new_board()
i = 1
def clientthread(conn, addr):
	# sends a message to the client whose user object is conn
    global i
    global board
    while True:
        winner = get_winner(board)
        for client in list_of_clients:
            if winner == 'X':
                client.send((Fore.GREEN + player1Name + " wins the game!").encode())
                break
            elif winner == 'O':
                client.send((Fore.GREEN + player2Name + " wins the game!").encode())
                break
            elif is_board_full(board, winner):
                client.send(("It's a draw!").encode())
                break
            else:
                client.send(("No winner yet").encode())
        #player1.send(str(i).encode())
        #player2.send(str(i).encode())
        if i % 2 == 1:
            coords_as_string = player1.recv(2048).decode()
        else:
            coords_as_string = player2.recv(2048).decode()
        coords = (int(coords_as_string[0]), int(coords_as_string[1]))
        b1 = board
        board = make_move(board, coords, i, player1, player2)
        if board != False:
            if i % 2 == 1:
                player1.send(("Board is making move").encode())
            else:
                player2.send(("Board is making move").encode())
        elif board == False:
            if i % 2 == 1:
                player1.send(("Board is False!").encode())
            else:
                player2.send(("Board is False!").encode())
        while board == False:
            if i % 2 == 1:
                player1.send(("Board is False").encode())
                coords_as_string = player1.recv(2048).decode()
            else:
                player2.send(("Board is False").encode())
                coords_as_string = player2.recv(2048).decode()
            coords = (int(coords_as_string[0]), int(coords_as_string[1]))
            board = make_move(b1, coords, i, player1, player2)
        listData = renderListString(board)
        broadcast(listData)
        i += 1


"""
Using the below function, we broadcast the message to all
clients
"""
def broadcast(listData):
    for client in list_of_clients:
        try:
            for line in listData:
                client.send(line.encode())
                #print(line)
        except:
            client.close()
            # if the link is broken, we remove the client
            remove(client)

"""
The following function simply removes the object
from the list that was created at the beginning of
the program
"""
def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)

while True:
    """
    Accepts a connection request and stores two parameters,
    conn which is a socket object for that user, and addr
    which contains the IP address of the client that jus
    connected
    """
    conn, addr = server_socket.accept()
    """
    Maintains a list of clients for ease of broadcasting
    a message to all available people in the chatroom
    """
    list_of_clients.append(conn)
    # prints the address of the user that just connected
    print(addr[0] + " connected")

    if len(list_of_clients) == 2:
        player1 = list_of_clients[0]
        player2 = list_of_clients[1]
        player1.send(str(1).encode())
        player2.send(str(2).encode())
        player1.send(("Welcome to Tic-Tac-Toe. The rules are the same, and you can type ''exit'' if you want to forfeit.").encode())
        player2.send(("Welcome to Tic-Tac-Toe. The rules are the same, and you can type ''exit'' if you want to forfeit.").encode())
        player_names.append(player1.recv(2048).decode())
        player_names.append(player2.recv(2048).decode())
        player1Name = player_names[0]
        player2Name = player_names[1]
        listData = renderListString(board)
        broadcast(listData)
        start_new_thread(clientthread,(conn,addr))
        print('yo')

conn.close()
server_socket.close()
