import sys
import socket
import select
import sys
from _thread import *
import threading
import pickle
from colorama import Fore, Back, Style
import list

class Client2:
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

if __name__ == "__main__":
    j = 2
    client = Client2(socket.gethostname())
    list.connected_client_objects.append(client)
    while True:
        j += 1
        print(len(list.connected_client_objects))
