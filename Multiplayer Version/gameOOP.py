import sys
import socket
import select
import sys
from _thread import *
import threading
import pickle
from colorama import Fore, Back, Style
from client import Client
from server import Server
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

'''
def run_game():
    # basically, this is just one file to run the program. We could run it in two separate files as a server.py, client.py, and a game.py, but let's just do it in one
    # so sys.argv just checks the command line for the nth argument or phrase or string in the command line, so sys.argv[1] is second phrase or text or argument on the command line
    # so if we want to run the file from the POV of the client, we have to do game.py 10.0.0.63 where 10.0.0.63 is the IP address we connect to because that is the IP address of where our server socket connects to and our server is hosted on
    if (len(sys.argv) > 1):
        # this is from client POV
        # client = Client(socket.gethostname())
        client = Client(sys.argv[1])
    else:
        # this is from server POV
        # this is the main run game logic
        server = Server()
        server.run()
        if len(server.connections) == 2:
            player1 = server.connections[0]
            player2 = server.connections[1]
'''

#connected_client_objects = []
if __name__ == '__main__':
    #list.init()
    def run_game():
        server_side = Server()
        server_side.run()
        while len(server_side.connections) == 2:
            if len(list.connected_client_objects) == 2:
                print(len(list.connected_client_objects))
                player1_object = list.connected_client_objects[0]
                player2_object = list.connected_client_objects[1]
                player1_socket = server_side.connections[0]
                player2_socket = server_side.connections[1]

    run_game()
