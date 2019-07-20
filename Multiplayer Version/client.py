# Python program to implement client side of chat room.
import socket
import select
import sys
from colorama import Fore, Back, Style


server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
server_sock.connect((socket.gethostname(), 5555))

name_for_client = ""

turn = server_sock.recv(2048).decode()
k = int(turn)

intro_message = server_sock.recv(2048).decode()
print(intro_message)
if k % 2 == 1:
    player1Nam = input("Player 1 (X), Enter in your name: ")
    name_for_client = player1Nam
    server_sock.send(player1Nam.encode())
else:
    player2Nam = input("Player 2 (O), Enter in your name: ")
    name_for_client = player2Nam
    server_sock.send(player2Nam.encode())

def get_move(name):
    x_coord = input(name + ": What is your move's X coordinate? ")
    y_coord = input(name + ": What is your move's Y coordinate? ")
    if "exit" in x_coord or "exit" in y_coord:
        print(Fore.RED + "Aww, you forfeited!")
        sys.exit()
    try:
        coordinates = (int(x_coord), int(y_coord))
    except ValueError:
        print("You didn't type in a number! Try again, %s." % name)
        return False
    return coordinates
#print(get_move())

while True:
    list_lines = []
    for j in range(0, 6):
        current_line = server_sock.recv(2048).decode()
        list_lines.append(current_line)
    for j in list_lines:
        print(j)
    if_winner = server_sock.recv(2048).decode()
    turn = int(server_sock.recv(2048).decode())
    if (i % 2) == (turn % 2):
        print(turn, if_winner)
        if if_winner == "No winner yet":
            coordinates = get_move(name_for_client)
            while coordinates == False:
                coordinates = get_move(name_for_client)
            coordinates_as_string = str(coordinates[0]) + str(coordinates[1])
            server_sock.send(coordinates_as_string.encode())
            invalid_or_valid_message = server_sock.recv(2048).decode()
            if invalid_or_valid_message == ("Valid Move!"):
                print(invalid_or_valid_message)
            board_status = server_sock.recv(2048).decode()
            if board_status == "Board is False!":
                b_status_again = server_sock.recv(2048).decode()
                while b_status_again == "Board is False":
                    coordinates = get_move(name_for_client)
                    while coordinates == False:
                        coordinates = get_move(name_for_client)
                    coordinates_as_string = str(coordinates[0]) + str(coordinates[1])
                    server_sock.send(coordinates_as_string.encode())
                    upd = server_sock.recv(2048).decode()
                    if upd and upd == "Board is False":
                        b_status_again = upd
        list_lines = []
        for i in range(0, 6):
            current_line = server_sock.recv(2048).decode()
            list_lines.append(current_line)
        for i in list_lines:
            print(i)
        else:
            print(if_winner)
            break


server_sock.close()
