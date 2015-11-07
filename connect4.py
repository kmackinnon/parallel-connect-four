#!/usr/bin/env python
import sys
import copy
from minimaxAI import run_AI as startMinimax
from randomAI import run_AI as startRandom

class Connect4(object):
    #index by (row,col), (0,0) is top left
    board = [["  " for x in range(7)] for y in range(6)]
    activePlayer = 0

    def __init__(self):
        pass

    def start(self):
        print "Welcome to Connect 4!"
        gameType = self.get_game_type()
        if gameType == "1":
            self.start_human_human_game()
        elif gameType == "2":
            self.start_human_computer_game()
        elif gameType == "3":
            self.start_computer_computer_game()
        else:
            print "Unexpected game type, exiting.."
            sys.exit()

    def get_game_type(self):
        while(True):
            print "\nChoose your game type:\n1. Human vs human\n2. Human vs computer\n3. Computer vs Computer"
            print ">>",
            gameChoice = get_single_character()
            if gameChoice not in ["1", "2", "3"]:
                print "You must enter the number for the desired game type"
                continue
            else:
                break
        return gameChoice

    def print_game_board(self):
        print "\nCURRENT GAME BOARD:\n"
        print "  0   1   2   3   4   5   6 "
        for i,row in enumerate(self.board):
            print " --- --- --- --- --- --- ---"
            print "|",
            for j,val in enumerate(row):
                if j != len(row)-1:
                    print val + "|",
                else:
                    print val + "|"
        print " --- --- --- --- --- --- ---\n"

    def make_move(self, col):
        if self.activePlayer == 0:
            valToWrite = "X"
        else:
            valToWrite = "O"

        for i in range(6):
            if self.board[i][col] == "  ":
                if i == 5:
                    self.board[i][col] = valToWrite + " "
                    return True
            else:
                if i == 0:
                    return False
                else:
                    self.board[i-1][col] = valToWrite + " "
                    return True

    def start_human_human_game(self):
        printBoard = True
        while(True):
            if printBoard:
                self.print_game_board()
                print "Enter column number to drop piece"

            if self.activePlayer == 0:
                print "Player 1 (X) >> ",
            else:
                print "Player 1 (O) >> ",

            colChoice = get_single_character()
            if colChoice == "k":
                sys.exit(0)
            elif colChoice not in ["0", "1", "2", "3", "4", "5", "6"]:
                print "You must enter a valid column"
                printBoard = False
                continue
            else:
                moveSuccess = self.make_move(int(colChoice))
                if moveSuccess:
                    self.activePlayer = (self.activePlayer + 1) % 2
                    printBoard = True
                else:
                    print "Invalid move, column full"
                    printBoard = False
                    continue


    def start_human_computer_game(self):
		printBoard = True
		while(True):
			if printBoard:
				self.print_game_board()

			count = 0
			for y in range(7):
				if self.board[0][y] == "X " or self.board[0][y] == "O ":
					count = count+1

			isFull = (count==7)
			if isFull:
				print "GAME BOARD IS FULL"
				break

			if self.activePlayer == 0:
				print "Enter column number to drop piece"
				print "Player 1 (X) >> "
				colChoice = get_single_character()
			else:
				print "Player 1 (O) >> "
				tempBoard = copy.deepcopy(self.board)
				colChoice = startMinimax(tempBoard, self.activePlayer)
				print "AI PLAYING COLUMN: " + colChoice

			if colChoice == "k":
				sys.exit(0)
			elif colChoice not in ["0", "1", "2", "3", "4", "5", "6"]:
				print "You must enter a valid column"
				printBoard = False
				continue
			else:
				moveSuccess = self.make_move(int(colChoice))
				if moveSuccess:
					self.activePlayer = (self.activePlayer + 1) % 2
					printBoard = True
				else:
					print "Invalid move, column full"
					printBoard = False
					continue

    def start_computer_computer_game(self):
        #TODO
		printBoard = True
		while(True):
			if printBoard:
				self.print_game_board()

			count = 0
			for y in range(7):
				if self.board[0][y] == "X " or self.board[0][y] == "O ":
					count = count+1
			isFull = (count==7)
			if isFull:
				print "GAME BOARD IS FULL"
				break

			tempBoard = copy.deepcopy(self.board)
			if self.activePlayer == 0:
				colChoice = startMinimax(tempBoard, self.activePlayer)
			else:
				colChoice = startMinimax(tempBoard, self.activePlayer)

			if colChoice == "k":
				sys.exit(0)
			elif colChoice not in ["0", "1", "2", "3", "4", "5", "6"]:
				print "AI player #" + str(self.activePlayer) + " did not choose a valid column"
				printBoard = False
				continue
			else:
				moveSuccess = self.make_move(int(colChoice))
				if moveSuccess:
					self.activePlayer = (self.activePlayer + 1) % 2
					printBoard = True
				else:
					print "AI player #" + str(self.activePlayer) + " did not make a valid move, column full"
					printBoard = False
					continue


def get_single_character():
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    print ch
    return ch

if __name__ == "__main__":
    game = Connect4()
    game.start()
