import sys
import socket
import select
import sys
from _thread import *
import threading
import pickle
from colorama import Fore, Back, Style
import list

'''
This is an OOP designed game. We have two classes: a Server class and a Client class. Ideally, we have one server and two clients connected to it.
The server keep tracks of the whole game and all the game logic and the board and everything. In the client class, it
has an instance variable which is its ID to distinguish between player 1 and player 2. Each client connected is an instance of the
Client class/an object. The server keeps track of turns and all the client really does is send the move to the server socket object
while the server sends the board back to each client and each client prints it. Make sure the board is owned by the Server object.
Here's the main flow of how run_game() in this version should look: create Server object and socket, for each new connection to the socket,
create a Client object, so now we have 1 Server socket and 2 Client sockets. Server sends all clients the empty board and all clients print that
empty board along with the intro welcome message. Then, All clients prompt users
for the names, and the clients send the names to the server which adds those names to a list it now owns of the player names.
Now, in the main run function, it keeps track of the turn count (i) for alternating turns
and in the while loop, run the get_winner() server instance method and is_board_full() server instance method
on the server instance board, and follow the standard procedure for that with all the messages and stuff and break if there's
a winner or if the board is full, and then move onto the main part, where the client who's ID % 2 == Turn % 2 asks user for the move
and it goes through that whole list and stuff from the main.py in Game with AI Folder in Tic-Tac-Toe Folder under Projects under Python in the Flashdrive.

You don't really need threading for this honestly because put simply and following KISS logic, just make it simple in a single thread.
'''

'''
Use Python's pickle module to send objects. Here's the basics:
d = {1: "Hey", 2 : "There"}
msg = pickle.dumps(d) # this pickles it
print(msg) # this prints msg in bytes serialization format, so you don't even need to do encode or decode cause it's already a bytes object

on the other side
d = pickle.loads(msg)
print(d)
'''

class Server:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connections = []

    def __init__(self):
        self.PORT = 5555
        self.moves = self.new_board()
        self.server_socket.bind((socket.gethostname(), self.PORT))
        self.server_socket.listen(2)
        print("Waiting for a connection, Server Started")

    def new_board(self):
        #l = [[None] * 3] * 3 doesn't work because replicating a list with * doesn’t create copies, it only creates references to the existing objects, so it makes copies of the first list and you can't edit
        l = [None] * 3
        for i in range(0, len(l)):
            # you now generate 3 different lists
            l[i] = [None] * 3
        return l

    # we only allow for two connections at max
    def run(self):
        while True:
            conn, addr = self.server_socket.accept()
            self.connections.append(conn)
            #print(self.connections)
            print(str(addr[0]) + ":" + str(addr[1]), "connected")

    def make_move(self, board, coords, num, player1, player2):
        # we could update the given board or just return a new board, let's do the latter because it might be easier to work with
        if num % 2 == 1:
            turn = "X"
        else:
            turn = "O"
        new_board = board
        if num % 2 == 1:
            if coords[0] >= len(board) or coords[1] >= len(board[0]):
                player1.send(("Invalid move! Your choice is off the grid. Try again.").encode())
                return False
            elif board[coords[0]][coords[1]] == " ":
                new_board[coords[0]][coords[1]] = turn
                return new_board
            else:
                player1.send(("Invalid move! That spot is already taken. Try again.").encode())
                return False
        else:
            if coords[0] >= len(board) or coords[1] >= len(board[0]):
                player2.send(("Invalid move! Your choice is off the grid. Try again.").encode())
                return False
            elif board[coords[0]][coords[1]] == " ":
                new_board[coords[0]][coords[1]] = turn
                return new_board
            else:
                player2.send(("Invalid move! That spot is already taken. Try again.").encode())
                return False

    def get_winner(self, board):
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

    def is_board_full(self, board, possible_winner):
        if possible_winner == None:
            sum = 0
            for i in range(0, len(board)):
                for j in range(0, len(board[0])):
                    if board[i][j] == 'X' or board[i][j] == 'O':
                        sum += 1
            if sum == len(board) * len(board[0]):
                return True

class Client:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, address):
        self.PORT = 5555
        self.server_socket.connect((address, self.PORT))
        print("Welcome to Tic-Tac-Toe. The rules are the same, and you can type ''exit'' if you want to forfeit.")
        self.render([[None, None, None], [None, None, None], [None, None, None]])

    def setIDandName(self, ID):
        self.player_Num = ID
        if self.player_Num % 2 == 1:
            self.name = input("Player 1 (X), Enter in your name: ")
        else:
            self.name = input("Player 2 (O), Enter in your name: ")

    def render(self, board):
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

    def get_move(self):
        x_coord = input(self.name + ": What is your move's X coordinate? ")
        y_coord = input(self.name + ": What is your move's Y coordinate? ")
        if "exit" in x_coord or "exit" in y_coord:
            #print(Fore.RED + "Aww, you forfeited! %s wins!" % player2Name)
            print(Fore.RED + "Aww, you forfeited!")
            sys.exit()
        try:
            coords = (int(x_coord), int(y_coord))
        except ValueError:
            print("You didn't type in a number! Try again.")
            return False
        return coords
    #print(get_move())


#connected_client_objects = []
if __name__ == '__main__':
    def run_game():
        # basically, this is just one file to run the program. We could run it in two separate files as a server.py, client.py, and a game.py, but let's just do it in one
        # so sys.argv just checks the command line for the nth argument or phrase or string in the command line, so sys.argv[1] is second phrase or text or argument on the command line
        # so if we want to run the file from the POV of the client, we have to do game.py 10.0.0.63 where 10.0.0.63 is the IP address we connect to because that is the IP address of where our server socket connects to and our server is hosted on
        if (sys.argv[1] == 'server'):
            # this is from server POV
            # this is the main run game logic
            server_side = Server()
            server_side.run()
            while len(server_side.connections) == 2:
                print(server_side.server_socket.recv(1024).decode())
                print(server_side.server_socket.recv(1024).decode())
                if len(list.connected_client_objects) == 2:
                    print(len(connected_client_objects))
                    player1_object = connected_client_objects[0]
                    player2_object = connected_client_objects[1]
                    player1_socket = server_side.connections[0]
                    player2_socket = server_side.connections[1]
        elif (sys.argv[1] == 'p1'):
            # this is from client POV
            #client = Client(sys.argv[1])
            client = Client(socket.gethostname())
            list.connected_client_objects.append(client)
            client.server_socket.send("yo".encode())
        elif (sys.argv[1] == 'p2'):
            client2 = Client(socket.gethostname())
            list.connected_client_objects.append(client2)
            client2.server_socket.send("yo".encode())


    run_game()
