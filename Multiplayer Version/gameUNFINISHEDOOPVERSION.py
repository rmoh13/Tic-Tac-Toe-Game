
class Player:
    def __init__(self, name, color, num):
        self.moves = new_board()
        self.name = name
        self.color = color
        self.num = num
        self.net = Network()

    def new_board():
        #l = [[None] * 3] * 3 doesn't work because replicating a list with * doesn’t create copies, it only creates references to the existing objects, so it makes copies and you can't edit
        l = [None] * 3
        for i in range(0, len(l)):
            # you now generate 3 different lists
            l[i] = [None] * 3
        return l

    def make_move(self, coords, num):
        # we could update the given board or just return a new board, let's do the latter because it might be easier to work with
        if num % 2 == 1:
            turn = "X"
        else:
            turn = "O"
        if coords[0] >= len(self.moves) or coords[1] >= len(self.moves[0]):
            print("Invalid move! Your choice is off the grid. Try again.")
            return False
        elif self.moves[coords[0]][coords[1]] == " ":
            self.moves[coords[0]][coords[1]] = turn
            return self.moves
        else:
            print("Invalid move! That spot is already taken. Try again.")
            return False

    def render(self):
        print("   0   1   2")
        for i in range(0, len(self.moves)):
            for j in range(0, len(self.moves[0])):
                if self.moves[i][j] == None:
                    self.moves[i][j] = " "
        for i in range(0, len(self.moves)):
            for j in range(0, len(self.moves[0])):
                if self.moves[i][j] == 'X':
                    self.moves[i][j] = u"\u001b[36mX"
                elif self.moves[i][j] == 'O':
                    self.moves[i][j] = u"\u001b[33mO"
        # this manual way is actually quicker and simpler than a complicated for loop with an if-else statement inside
        # we're formatting this a bit differently as x,y coordinates
        print(u"\u001b[37m0  " + self.moves[0][0] + u"\u001b[37m | " + self.moves[1][0] + u"\u001b[37m | " + self.moves[2][0])
        line = [u"\u001b[37m_" for i in range(0, len(self.moves[0])+8)]
        print("  " + "".join(line))
        print(u"\u001b[37m1  " + self.moves[0][1] + u"\u001b[37m | " + self.moves[1][1] + u"\u001b[37m | " + self.moves[2][1])
        print("  " + "".join(line))
        print(u"\u001b[37m2  " + self.moves[0][2] + u"\u001b[37m | " + self.moves[1][2] + u"\u001b[37m | " + self.moves[2][2])

    def renderListString(self):
        # this is basically useful for when we want to send this data to the server
        firstLine = "   0   1   2"
        for i in range(0, len(self.moves)):
            for j in range(0, len(self.moves[0])):
                if self.moves[i][j] == None:
                    self.moves[i][j] = " "
        for i in range(0, len(self.moves)):
            for j in range(0, len(self.moves[0])):
                if self.moves[i][j] == 'X':
                    self.moves[i][j] = u"\u001b[36mX"
                elif self.moves[i][j] == 'O':
                    self.moves[i][j] = u"\u001b[33mO"
        # this manual way is actually quicker and simpler than a complicated for loop with an if-else statement inside
        # we're formatting this a bit differently as x,y coordinates
        secondLine = u"\u001b[37m0  " + self.moves[0][0] + u"\u001b[37m | " + self.moves[1][0] + u"\u001b[37m | " + self.moves[2][0]
        line = [u"\u001b[37m_" for i in range(0, len(self.moves[0])+8)]
        thirdLine = "  " + "".join(line)
        fourthLine = u"\u001b[37m1  " + self.moves[0][1] + u"\u001b[37m | " + self.moves[1][1] + u"\u001b[37m | " + self.moves[2][1]
        fifthLine = "  " + "".join(line)
        sixthLine = u"\u001b[37m2  " + self.moves[0][2] + u"\u001b[37m | " + self.moves[1][2] + u"\u001b[37m | " + self.moves[2][2]
        finalList = [firstLine, secondLine, thirdLine, fourthLine, fifthLine, sixthLine]
        return finalList

    def get_name(self):
        return self.name

    def get_num(self):
        return self.num

class Game:
    def __init__(self, player1Name, player2Name, color1, color2):
        self.player = Player(player1Name, color1, 1)
        self.player2 = Player(player2Name, color2, 2)
        #self.wins = [0,0]
        #self.ties = 0

    def get_move1(self):
        # num represents which player is playing, so num = 1 or odd number is Player 1, and num = 2 or even number is Player 2, and num starts from 1 not zero
        x_coord = input(self.player.get_name() + ": What is your move's X coordinate? ")
        y_coord = input(self.player.get_name() + ": What is your move's Y coordinate? ")
        if "exit" in x_coord or "exit" in y_coord:
            print(Fore.RED + "Aww, you forfeited! %s wins!" % self.player2.get_name())
            sys.exit()
        try:
            coords = (int(x_coord), int(y_coord))
        except ValueError:
            print("You didn't type in a number! Try again.")
            return False
        return coords
    #print(get_move())

    def get_move2(self):
        # num represents which player is playing, so num = 1 or odd number is Player 1, and num = 2 or even number is Player 2, and num starts from 1 not zero
        x_coord = input(self.player2.get_name()elf.name + ": What is your move's X coordinate? ")
        y_coord = input(self.player2.get_name() + ": What is your move's Y coordinate? ")
        if "exit" in x_coord or "exit" in y_coord:
            print(Fore.RED + "Aww, you forfeited! %s wins!" % self.player.get_name())
            sys.exit()
        try:
            coords = (int(x_coord), int(y_coord))
        except ValueError:
            print("You didn't type in a number! Try again.")
            return False
        return coords
    #print(get_move())

    # in the main run method, we're gonna have to make sure that self.player.moves == self.player2.moves
    def get_winner(self):
        #list_all_lines = board doesn't work because it's still referencing board and is gonna change both board and list_all_lines, but we only wanna change list_all_lines as lists are mutable objects
        list_all_lines = []
        [list_all_lines.append(i) for i in self.player.moves]
        diag1 = []
        diag1.append(self.player.moves[0][0])
        diag1.append(self.player.moves[1][1])
        diag1.append(self.player.moves[2][2])
        list_all_lines.append(diag1)
        diag2 = []
        diag2.append(self.player.moves[0][2])
        diag2.append(self.player.moves[1][1])
        diag2.append(self.player.moves[2][0])
        list_all_lines.append(diag2)

        for i in range(0, len(self.player.moves[0])):
            col = []
            for j in range(0, len(self.player.moves)):
                col.append(self.player.moves[j][i])
            list_all_lines.append(col)
        #print(list_all_lines)
        winner = None
        for i in range(0, len(list_all_lines)):
            # sets must have distinct elements
            if type(list_all_lines[i][0]) == str and len(set(list_all_lines[i])) == 1:
                winner = list_all_lines[i][0]
        return winner

    def is_board_full(self, possible_winner):
        if possible_winner == None:
            sum = 0
            for i in range(0, len(self.player.moves)):
                for j in range(0, len(self.player.moves[0])):
                    if self.player.moves[i][j] == 'X' or self.player.moves[i][j] == 'O':
                        sum += 1
            if sum == len(self.player.moves) * len(self.player.moves[0]):
                return True

    def run_game():
        board = new_board()
        render(board)
        print("Welcome to Tic-Tac-Toe. The rules are the same, and you can type ''exit'' if you want to forfeit.")
        player1Name = input("Player 1 (X), Enter in your name: ")
        player2Name = input("Player 2 (O), Enter in your name: ")
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

    def send_data1(self):
        listData = self.player.renderListString()
        for i in listData:
            reply = self.net.send(i)
        return reply

    def send_data2(self):
        listData2 = self.player2.renderListString()
        reply2 = self.net.send(listData2)
        return reply2
