import sys
import socket
import select
import sys
from _thread import *
import threading
import pickle
from colorama import Fore, Back, Style

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
        j = 1
        while j <= 2:
            conn, addr = self.server_socket.accept()
            self.connections.append(conn)
            #print(self.connections)
            print(str(addr[0]) + ":" + str(addr[1]), "connected")
            j += 1

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
