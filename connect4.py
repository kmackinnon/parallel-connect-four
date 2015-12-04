#!/usr/bin/env python
import sys
import copy
from getch import getch
from minimaxAIParallel import run_AI as startPar
from minimaxAISequential import run_AI as startSeq
from minimaxCommon import evaluateBoard
from randomAI import run_AI as startRandom
from gameover import gameOver
from random import randint
import time

class Connect4(object):

    HEIGHT = 6
    WIDTH = 7
    FIRST = True

    #index by (row,col), (0,0) is top left
    board = [[" " for x in range(WIDTH)] for y in range(HEIGHT)]
    activePlayer = 0

    def __init__(self):
        pass

    def start(self):
        print "Welcome to Connect 4!"
        self.activePlayer = randint(0,1)
        gameType = self.get_game_type()
        if gameType == "1":
            self.start_human_human_game()
        elif gameType == "2":
            self.start_human_computer_game(False)
        elif gameType == "3":
            self.start_human_computer_game(True)
        elif gameType == "4":
            self.start_computer_computer_game()
        else:
            print "Unexpected game type, exiting.."
            sys.exit()

    def get_game_type(self):
        while(True):
            print ("\nChoose your game type:\n1. Human vs Human\n2. Human vs Serial Computer" +
            "\n3. Human vs Parallel Computer\n4. Computer vs Computer")
            print ">>",
            gameChoice = getch()
            if gameChoice not in ["1", "2", "3", "4"]:
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
                    if val != " ":
                        print val + " |",
                    else:
                        print val + " |",
                else:
                    if val != " ":
                        print val + " |"
                    else:
                        print val + " |"
        print " --- --- --- --- --- --- ---\n"

    def make_move(self, col):
        # first player is player 0
        if self.activePlayer == 0:
            valToWrite = "X"
        else:
            valToWrite = "O"

        for i in range(self.HEIGHT):
            if self.board[i][col] == " ":
                if i == 5:
                    self.board[i][col] = valToWrite
                    return True
            else:
                if i == 0:
                    return False
                else:
                    self.board[i-1][col] = valToWrite
                    return True

    def start_human_human_game(self):
        printBoard = True
        tie = True

        # game loop
        while(True):
            if printBoard:
                self.print_game_board()
                print "Enter column number to drop piece"

            if self.activePlayer == 0:
                print "Player 1 (X) >> ",
            else:
                print "Player 2 (O) >> ",

            colChoice = getch()
            if colChoice == "k":
                sys.exit(0)
            elif colChoice not in [str(x) for x in range(self.WIDTH)]:
                print "You must enter a valid column"
                printBoard = False
                continue
            else:
                moveSuccess = self.make_move(int(colChoice))
                if moveSuccess:
                    evaluateBoard(self.board, self.activePlayer)
                    if gameOver(self.board, self.activePlayer):
                        print "PLAYER %d WON!\n" % (self.activePlayer+1)
                        tie = False
                        break
                    self.activePlayer = (self.activePlayer + 1) % 2
                    printBoard = True
                else:
                    print "Invalid move, column full"
                    printBoard = False
                    continue
        #final game board
        self.print_game_board()
        if tie:
            print "GAME WAS A TIE\n"

    def start_human_computer_game(self, is_parallel):
        printBoard = True
        tie = True

        # game loop
        while(True):
            if printBoard:
                self.print_game_board()

            count = 0
            for y in range(self.WIDTH):
                if self.board[0][y] == "X" or self.board[0][y] == "O":
                    count += 1

            isFull = (count==self.WIDTH)
            if isFull:
                break

            if self.activePlayer == 0:
                print "Enter column number to drop piece"
                print "Player 1 (X) >> "
                colChoice = getch()
                self.FIRST = False
            else:
                print "Player 2 (O) >> "
                if self.FIRST:
                    colChoice = "3"
                    self.FIRST = False
                else:
                    tempBoard = copy.deepcopy(self.board)
                    st = time.time()
                    
                    if is_parallel:
                        colChoice = startPar(tempBoard, self.activePlayer)
                    else:
                        colChoice = startSeq(tempBoard, self.activePlayer)
                    
                    et = time.time()
                    print "[INFO] Time taken: " + str(et - st)
                print "[INFO] AI is playing column " + colChoice

            if colChoice == "k":
                sys.exit(0)
            elif colChoice not in [str(x) for x in range(self.WIDTH)]:
                print "You must enter a valid column"
                printBoard = False
                continue
            else:
                moveSuccess = self.make_move(int(colChoice))
                if moveSuccess:
                    if gameOver(self.board, self.activePlayer):
                        print "PLAYER %d WON!\n" % (self.activePlayer+1)
                        tie = False
                        break
                    self.activePlayer = (self.activePlayer + 1) % 2
                    printBoard = True
                else:
                    print "Invalid move, column full"
                    printBoard = False
                    continue
        self.print_game_board()
        if tie:
            print "GAME WAS A TIE\n"

    def start_computer_computer_game(self):
        printBoard = True
        tie = True

        # game loop
        while(True):
            if printBoard:
                self.print_game_board()

            count = 0
            for y in range(self.WIDTH):
                if self.board[0][y] == "X" or self.board[0][y] == "O":
                    count += 1
            isFull = (count==self.WIDTH)
            if isFull:
                break

            tempBoard = copy.deepcopy(self.board)
            if self.activePlayer == 0:
                if self.FIRST:
                    colChoice = "3"
                    self.FIRST = False
                else:
                    st = time.time()
                    colChoice = startPar(tempBoard, self.activePlayer)
                    et = time.time()
            else:
                if self.FIRST:
                    colChoice = "3"
                    self.FIRST = False
                else:
                    st = time.time()
                    colChoice = startSeq(tempBoard, self.activePlayer)
                    et = time.time()

            if colChoice == "k":
                sys.exit(0)
            elif colChoice not in [str(x) for x in range(self.WIDTH)]:
                print "[ERROR] AI player #" + str(self.activePlayer) + " did not choose a valid column"
                printBoard = False
                continue
            else:
                moveSuccess = self.make_move(int(colChoice))
                if moveSuccess:
                    if gameOver(self.board, self.activePlayer):
                        print "PLAYER %d WON!\n" % (self.activePlayer)
                        tie = False
                        break
                    self.activePlayer = (self.activePlayer + 1) % 2
                    printBoard = True
                else:
                    print "[ERROR] AI player #" + str(self.activePlayer) + " did not make a valid move, column full"
                    printBoard = False
                    continue
        #final game board
        self.print_game_board()
        if tie:
            print "GAME WAS A TIE\n"


if __name__ == "__main__":
    game = Connect4()
    game.start()
