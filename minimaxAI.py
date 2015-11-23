import sys
import copy
import time
import multiprocessing
from functools import partial
from gameover import gameOver
import my_thread as t
import evaluationUtilities as util

activePlayer = -1
opponentPlayer = -1
maxTime = 10
startTime = 0
maxDepth = 7

# returns an action
def alpha_beta_search(board):
    global startTime
    startTime = time.clock()
    moves = get_moves(board)
    v = max_value_first(board, float('-inf'), float('inf'), 0)
    return v[1]

# returns a utility value
def max_value_first(board, alpha, beta, depth):
    v = float('-inf')
    moves = get_moves(board);
    
    v_mins = []

    iterable = [ x for x in moves ]
    print iterable
    pool = multiprocessing.Pool()
    func = partial(t.find_min, board,activePlayer,alpha,beta,depth)
    v_mins = pool.map(func, iterable)
    pool.close()
    pool.join()

    v = max(v_mins)
    move = v_mins.index(v)

    print v_mins
    print "VAL: " , v
    print "MOVE: ", move

    return (v, move)

# returns a utility value
def max_value(board, alpha, beta, depth):
    if terminal_test(board, opponentPlayer, depth):
        return utility(board)
    v = float('-inf')
    for a in get_moves(board):
        v = max(v, min_value(make_move(board,a,activePlayer), alpha, beta, depth+1))
        if v >= beta:
            return v
        alpha = max(alpha,v)
    return v

def min_value(board, alpha, beta, depth):
    if terminal_test(board, activePlayer, depth):
        return utility(board)
    v = float('inf')
    for a in get_moves(board):
        v = min(v, max_value(make_move(board,a,opponentPlayer), alpha, beta, depth+1))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v

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
def timeCheck():
    endTime = time.clock()
    if (endTime - startTime) >= maxTime:
        return True
    else:
        return False

# Checks if player has won or board is full
# Returns true if terminal has been reached
def terminal_test(board, player, depth):
    # checks if time limit has been reached
    if timeCheck():
        #print "[INFO] AI ran out of time."
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

# calculates the utility of a given board state
def utility(board):
    global activePlayer
    if activePlayer == 0:
        myValToCheck = "X"
        oppValToCheck = "O"
    else:
        myValToCheck = "O"
        oppValToCheck = "X"

    twoStreakMult = 1
    threeStreakMult = 5
    fourStreakMult = 30

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
    totalScore = 0
    totalScore += (twoStreakMult * (rowScore[2] + colScore[2] + upRightDiagScore[2] + upLeftDiagScore[2]))
    totalScore += (threeStreakMult * (rowScore[3] + colScore[3] + upRightDiagScore[3] + upLeftDiagScore[3]))
    totalScore += (fourStreakMult * (rowScore[4] + colScore[4] + upRightDiagScore[4] + upLeftDiagScore[4]))

    totalScore += -3 * (twoStreakMult * (oppRowScore[2] + oppColScore[2] + oppUpRightDiagScore[2] + oppUpLeftDiagScore[2]))
    totalScore += -3 * (threeStreakMult * (oppRowScore[3] + oppColScore[3] + oppUpRightDiagScore[3] + oppUpLeftDiagScore[3]))
    totalScore += -3 * (fourStreakMult * (oppRowScore[4] + oppColScore[4] + oppUpRightDiagScore[4] + oppUpLeftDiagScore[4]))
    #print "Total score for %s is %d\n" % (myValToCheck, totalScore)
    return totalScore

def evaluateBoard(board, player):
    activePlayer = player
    utility(board)

def run_AI(board, ID):
    global activePlayer
    global opponentPlayer
    activePlayer = ID
    if activePlayer == 0:
        opponentPlayer = 1
    else:
        opponentPlayer = 0
    v = alpha_beta_search(board)
    return str(v)

