import sys
import copy
import time
from gameover import gameOver
import evaluationUtilities as util

# Gets the moves available for the AI
# Returns a list of available columns that are playable
def get_moves(board):
    openSpaces = []
    for y in range(7):
        if board[0][y] != 'X' and board[0][y] != 'O':
            openSpaces.append(y)
    return openSpaces

# Makes a move given a board, a column to play, and the player
# Returns the board after the move has been played
def make_move(board, col, player):
    tempBoard = copy.deepcopy(board)
    if player == 0:
        valToWrite = "X"
    else:
        valToWrite = "O"
    for i in range(6):
        if tempBoard[i][col] == " ":
            if i == 5:
                tempBoard[i][col] = valToWrite
                return tempBoard
        else:
            if i != 0:
                tempBoard[i-1][col] = valToWrite
                return tempBoard

# Checks how much time has currently elapsed
# Return true if elapsed time is longer than max time
def time_check(startTime, maxTime):
    endTime = time.clock()
    if (endTime - startTime) >= maxTime:
        return True
    else:
        return False

# Checks if player has won or board is full
# Returns true if terminal has been reached
def terminal_test(board, player, depth, startTime, maxTime, maxDepth):
    # checks if time limit has been reached
    if time_check(startTime, maxTime):
        print "[INFO] AI ran out of time."
        return True

    # checks if max depth has been reached
    if depth >= maxDepth:
        #print "[INFO] AI reached the max depth"
        return True

    # checks if player has won
    if gameOver(board, player):
        return True

    # check if board is full
    count = 0
    for y in range(7):
        if board[0][y] == "X" or board[0][y] == "O":
            count += 1
    if (count==7):
       return True

    return False

def evaluateBoard(board, player):
    activePlayer = player
    utility(board)

# calculates the utility of a given board state
def utility(board, activePlayer):
    if activePlayer == 0:
        myValToCheck = "X"
        oppValToCheck = "O"
    else:
        myValToCheck = "O"
        oppValToCheck = "X"

    #key is number of values in streak, value is the number of streaks for that key
    rowScore = {2:0, 3:0, 4:0}
    colScore = {2:0, 3:0, 4:0}
    upRightDiagScore = {2:0, 3:0, 4:0}
    upLeftDiagScore = {2:0, 3:0, 4:0}

    # Opponent scores
    oppRowScore = {2:0, 3:0, 4:0}
    oppColScore = {2:0, 3:0, 4:0}
    oppUpRightDiagScore = {2:0, 3:0, 4:0}
    oppUpLeftDiagScore = {2:0, 3:0, 4:0}

    #check for vertical matches
    util.checkVerticalMatches(board, myValToCheck, colScore)
    util.checkVerticalMatches(board, oppValToCheck, oppColScore)

    #check for horizontal matches
    util.checkHorizontalMatches(board, myValToCheck, rowScore)
    util.checkHorizontalMatches(board, oppValToCheck, oppRowScore)

    # check upper right diagonal matches
    util.checkUpperRightDiagMatches(board, myValToCheck, upRightDiagScore)
    util.checkUpperRightDiagMatches(board, oppValToCheck, oppUpRightDiagScore)

    # check upper left diagonal matches
    util.checkUpperLeftDiagMatches(board, myValToCheck, upLeftDiagScore)
    util.checkUpperLeftDiagMatches(board, oppValToCheck, oppUpLeftDiagScore)
    '''
    print "\n==========================\nREPORT FOR %s VALUES\n==========================\n" % myValToCheck
    print "Valid vertical streaks:\n2:%d\n3:%d\n4:%d\n" % (colScore[2], colScore[3], colScore[4])
    print "Valid horizontal streaks:\n2:%d\n3:%d\n4:%d\n" % (rowScore[2],rowScore[3],rowScore[4])
    print "Valid northeast streaks:\n2:%d\n3:%d\n4:%d\n" % (upRightDiagScore[2], upRightDiagScore[3], upRightDiagScore[4])
    print "Valid northwest streaks:\n2:%d\n3:%d\n4:%d\n" % (upLeftDiagScore[2], upLeftDiagScore[3], upLeftDiagScore[4])
    print "\n==========================\nREPORT FOR %s VALUES\n==========================\n" % oppValToCheck
    print "Valid vertical streaks:\n2:%d\n3:%d\n4:%d\n" % (oppColScore[2], oppColScore[3], oppColScore[4])
    print "Valid horizontal streaks:\n2:%d\n3:%d\n4:%d\n" % (oppRowScore[2],oppRowScore[3],oppRowScore[4])
    print "Valid northeast streaks:\n2:%d\n3:%d\n4:%d\n" % (oppUpRightDiagScore[2], oppUpRightDiagScore[3], oppUpRightDiagScore[4])
    print "Valid northwest streaks:\n2:%d\n3:%d\n4:%d\n" % (oppUpLeftDiagScore[2], oppUpLeftDiagScore[3], oppUpLeftDiagScore[4])
    '''

    # Player mulitpliers
    twoStreakMult = 1
    threeStreakMult = 5
    fourStreakMult = 30

    # Opponent multipliers
    oppTwoStreakMult = -1
    oppThreeStreakMult = -5
    oppFourStreakMult = -30

    totalScore = 0
    totalScore += (twoStreakMult * (rowScore[2] + colScore[2] + upRightDiagScore[2] + upLeftDiagScore[2]))
    totalScore += (threeStreakMult * (rowScore[3] + colScore[3] + upRightDiagScore[3] + upLeftDiagScore[3]))
    totalScore += (fourStreakMult * (rowScore[4] + colScore[4] + upRightDiagScore[4] + upLeftDiagScore[4]))

    totalScore += (oppTwoStreakMult * (oppRowScore[2] + oppColScore[2] + oppUpRightDiagScore[2] + oppUpLeftDiagScore[2]))
    totalScore += (oppThreeStreakMult * (oppRowScore[3] + oppColScore[3] + oppUpRightDiagScore[3] + oppUpLeftDiagScore[3]))
    totalScore += (oppFourStreakMult * (oppRowScore[4] + oppColScore[4] + oppUpRightDiagScore[4] + oppUpLeftDiagScore[4]))
    #print "Total score for %s is %d\n" % (myValToCheck, totalScore)
    return totalScore
