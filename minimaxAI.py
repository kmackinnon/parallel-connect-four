import sys
import copy
import time
from gameover import gameOver
from random import randint

activePlayer = -1
maxTime = 10
startTime = 0
maxDepth = 7

# returns an action
def alpha_beta_search(board):
    global startTime
    startTime = time.clock()
    moves = get_moves(board)
    move = moves[randint(0,len(moves)-1)]
    # v = max_value(state, alpha, beta)
    v = max_value_first(board, float('-inf'), float('inf'), move, 0)
    return v[1]

# returns a utility value
def max_value_first(board, alpha, beta, m, depth):
    v = float('-inf')
    move = m
    for a in get_moves(board):
        vMin = min_value(make_move(board,a,activePlayer), alpha, beta, depth+1)
        if v >= vMin:
            move = a
        else:
            v = vMin
        if v >= beta:
            return (v, move)
        alpha = max(alpha,v)
    return (v, move)

# returns a utility value
def max_value(board, alpha, beta, depth):

    # set opponent
    if activePlayer == 0:
        player = 1
    else:
        player = 0

    if terminal_test(board, player) or timeCheck() or depth > maxDepth:
        return utility(board)
    v = float('-inf')
    for a in get_moves(board):
        v = max(v, min_value(make_move(board,a,activePlayer), alpha, beta, depth+1))
        if v >= beta:
            return v
        alpha = max(alpha,v)
    return v

def min_value(board, alpha, beta, depth):

    # set opponent
    if activePlayer == 0:
        player = 1
    else:
        player = 0

    if terminal_test(board, activePlayer) or timeCheck() or depth > maxDepth:
        return utility(board)
    v = float('inf')
    for a in get_moves(board):
        v = min(v, max_value(make_move(board,a,player), alpha, beta, depth+1))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v

def get_moves(board):
    openSpaces = []
    for y in range(7):
        if board[0][y] != 'X' and board[0][y] != 'O':
            openSpaces.append(y)
    return openSpaces

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

# checks if player has won or board is full
def terminal_test(board, player):
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

def timeCheck():
    endTime = time.clock()
    if (endTime - startTime) >= maxTime:
        print "AI OUT OF TIME"
        return True
    else:
        return False

def checkColumn(board, val, col):
    #only returns a count if there is an available slot above the streak of values

    #start from the botton and decrement counter
    counting = False
    count = 0
    for row in range(5, -1, -1):
        if board[row][col] == val:
            counting = True
            count += 1
        elif counting:
            counting = False
            if board[row][col] == " ":
                #if empty spot above, nothing else in this column
                if row == 0:
                    #top element in column is space, so count must be at least 3 for it to be valid
                    if count >= 3:
                        break
                    else:
                        count = 0
                elif row == 1:
                    #second highest element in column is space, so count must be at least 2, with 2 empty spaces above, to be valid
                    if count >= 2:
                        break
                    else:
                        count = 0
                else:
                    break
            else:
                #opponent value above streak, so dont want to include the count cause you cant do anything with this
                count = 0
    return count

def checkRow(board, val, row):
    leftSet = False
    leftIndices = []
    rightSet = False
    rightIndices = []
    retDict = {2:0, 3:0, 4:0}

    for col in range(7):
        if board[row][col] == val:
            if not leftSet:
                #the first occurence of the val in the row
                leftSet = True
                leftIndices.append(col)
        else:
            if leftSet and col != 0:
                #the last value in a streak
                rightIndices.append(col-1)

                #set to false to keep searching for more streaks
                leftSet = False

        if col == 6 and leftSet:
            #loop reached the end of a row without getting a space or opponent value, so this is the desired value
            rightIndices.append(col)

    #check each pair of indices to evaluate the score
    if len(leftIndices) != len(rightIndices):
        print "ROW CHECK ERROR"
    else:
        for i in range(len(leftIndices)):
            #check how many available spots on both sides of streak, if less than 4, then this is not a valid streak
            leftSpotsFree = 0
            rightSpotsFree = 0
            leftIndex = leftIndices[i]
            rightIndex = rightIndices[i]

            #add 1 to account for zero indexing
            streakLength = rightIndex - leftIndex + 1

            if streakLength < 2:
                #dont care about single value
                continue

            if leftIndex == 0:
                #obviously no left spots available
                pass
            elif leftIndex == 1:
                if board[row][leftIndex-1] == " ":
                    leftSpotsFree += 1
            else:
                #need at most 2 empty spots, since streaks < 2 haven't gotten this far
                if board[row][leftIndex-2] == " " and board[row][leftIndex-1] == " ":
                    leftSpotsFree += 2
                elif board[row][leftIndex-1] == " ":
                    leftSpotsFree += 1

            if rightIndex == 6:
                pass
            elif rightIndex == 5:
                if board[row][rightIndex+1] == " ":
                    rightSpotsFree += 1
            else:
                if board[row][rightIndex+2] == " " and board[row][rightIndex+1] == " ":
                    rightSpotsFree += 2
                elif board[row][rightIndex+1] == " ":
                    rightSpotsFree += 1

            if (streakLength + leftSpotsFree + rightSpotsFree) >= 4:
                #increment the number of streakLength streaks
                retDict[streakLength] += 1
    return retDict

def checkUpperRightDiagonals(board, val):
    checkBoard = [[False for x in range(7)] for y in range(6)]
    retDict = {2:0, 3:0, 4:0}

    leftColIndices = []
    rightColIndices = []
    topRowIndices = []
    bottomRowIndices = []

    #iterate through every element in the array. If desired value found, then look up and to the right,
    #then down to the left to get the end indices of the diagonal streak
    for row in range(6):
        for col in range(7):
            if board[row][col] == val:
                #avoid checking diagonals that have already been checked
                if not checkBoard[row][col]:
                    checkBoard[row][col] = True
                    tempRow = row
                    tempCol = col
                    counting = True

                    #check up and to the right
                    if row == 0 or col == 6:
                        rightColIndices.append(col)
                        topRowIndices.append(row)
                    else:
                        while(counting):
                            tempRow -= 1
                            tempCol += 1
                            if tempRow == 0 or tempCol == 6:
                                if board[tempRow][tempCol] == val:
                                    #value found at edge of matrix
                                    rightColIndices.append(tempCol)
                                    topRowIndices.append(tempRow)
                                    checkBoard[tempRow][tempCol] = True
                                else:
                                    #previous value in diagonal was end of streak
                                    rightColIndices.append(tempCol-1)
                                    topRowIndices.append(tempRow+1)

                                #at edge of matrix, so stop counting
                                counting = False
                            else:
                                #not at upper right edge of matrix
                                if board[tempRow][tempCol] == val:
                                    #just set this value to checked, and continue searching the diagonal
                                    checkBoard[tempRow][tempCol] = True
                                else:
                                    #previous value in diagonal was end of streak
                                    counting = False
                                    rightColIndices.append(tempCol-1)
                                    topRowIndices.append(tempRow+1)

                    #check down and to the left
                    if row == 5 or col == 0:
                        leftColIndices.append(col)
                        bottomRowIndices.append(row)
                    else:
                        counting = True
                        tempRow = row
                        tempCol = col
                        while(counting):
                            tempRow += 1
                            tempCol -= 1
                            if tempRow == 5 or tempCol == 0:
                                #at edge of matrix
                                if board[tempRow][tempCol] == val:
                                    #this is a desired value at the edge of the matrix
                                    checkBoard[tempRow][tempCol] = True
                                    leftColIndices.append(tempCol)
                                    bottomRowIndices.append(tempRow)
                                else:
                                    #edge of matrix, so previous value was desired
                                    leftColIndices.append(tempCol+1)
                                    bottomRowIndices.append(tempRow-1)
                                counting = False
                            else:
                                #not at edge of matrix
                                if board[tempRow][tempCol] == val:
                                    #just set this value to checked, and continue searching the diagonal
                                    checkBoard[tempRow][tempCol] = True
                                else:
                                    #previous value in diagonal was end of streak
                                    counting = False
                                    leftColIndices.append(tempCol+1)
                                    bottomRowIndices.append(tempRow-1)

    #iterate through sets of diagonal streak end points
    if len(leftColIndices) != len(rightColIndices) and len(leftColIndices) != len(topRowIndices) and len(leftColIndices) != len(bottomRowIndices):
        print "ERROR: upper right diagonal index lists not same size"
    else:
        #check each set of indices, each set represents one diagonal streak
        for i in range(len(leftColIndices)):
            leftIndex = leftColIndices[i]
            rightIndex = rightColIndices[i]
            topIndex = topRowIndices[i]
            bottomIndex = bottomRowIndices[i]

            if leftIndex == rightIndex:
                #single value, dont care about it
                continue
            else:
                streakLength = rightIndex - leftIndex + 1

                #check for free spots on either end of the streak
                leftFreeSpots = 0
                rightFreeSpots = 0

                #check free spots down and to the left
                if leftIndex == 0:
                    pass
                elif leftIndex == 1:
                    if bottomIndex != 5:
                        if board[bottomIndex+1][leftIndex-1] in (' ', val):
                            leftFreeSpots += 1
                else:
                    #look 2 cells in this direction
                    if bottomIndex != 4 and bottomIndex != 5:
                        #also consider val a free space when looking 2 cells away, to account for gaps
                        if board[bottomIndex+1][leftIndex-1] == ' ' and board[bottomIndex+2][leftIndex-2] in (' ', val):
                            leftFreeSpots += 2
                        elif board[bottomIndex+1][leftIndex-1] == ' ':
                            leftFreeSpots += 1
                    elif bottomIndex != 5:
                        #bottom index = 4
                        if board[bottomIndex+1][leftIndex-1] == ' ':
                            leftFreeSpots += 1

                #check free spots up and to the right
                if rightIndex == 6:
                    pass
                elif rightIndex == 5:
                    if topIndex != 0:
                        if board[topIndex-1][rightIndex+1] == ' ':
                            rightFreeSpots += 1
                else:
                    if topIndex != 1 and topIndex != 0:
                        if board[topIndex-1][rightIndex+1] == ' ' and board[topIndex-2][rightIndex+2] in (' ', val):
                            rightFreeSpots += 2
                        elif board[topIndex-1][rightIndex+1] == ' ':
                            rightFreeSpots += 1
                    elif topIndex != 0:
                        if board[topIndex-1][rightIndex+1] == ' ':
                            rightFreeSpots += 1

                if (streakLength + leftFreeSpots + rightFreeSpots) >= 4:
                    #a possible 4 in a row could occur, so increment the number of valid streaks
                    retDict[streakLength] += 1
    return retDict

def checkUpperLeftDiagonals(board, val):
    #Basically same algorithm as previous function, just with opposite orientation
    #look there for comments
    checkBoard = [[False for x in range(7)] for y in range(6)]
    retDict = {2:0, 3:0, 4:0}

    leftColIndices = []
    rightColIndices = []
    topRowIndices = []
    bottomRowIndices = []
    for row in range(6):
        for col in range(7):
            if board[row][col] == val:
                if not checkBoard[row][col]:
                    checkBoard[row][col] = True
                    tempRow = row
                    tempCol = col
                    counting = True
                    leftSet = False
                    rightSet = False

                    #check up and to the left
                    if row == 0 or col == 0:
                        leftColIndices.append(col)
                        topRowIndices.append(row)
                    else:
                        while(counting):
                            tempRow -= 1
                            tempCol -= 1
                            if tempRow == 0 or tempCol == 0:
                                if board[tempRow][tempCol] == val:
                                    leftColIndices.append(tempCol)
                                    topRowIndices.append(tempRow)
                                    checkBoard[tempRow][tempCol] = True
                                else:
                                    leftColIndices.append(tempCol+1)
                                    topRowIndices.append(tempRow+1)
                                counting = False
                            else:
                                if board[tempRow][tempCol] == val:
                                    checkBoard[tempRow][tempCol] = True
                                else:
                                    counting = False
                                    leftColIndices.append(tempCol+1)
                                    topRowIndices.append(tempRow+1)

                    #check down and to the right
                    if row == 5 or col == 6:
                        rightColIndices.append(col)
                        bottomRowIndices.append(row)
                    else:
                        counting = True
                        tempRow = row
                        tempCol = col
                        #check down and to the left
                        while(counting):
                            tempRow += 1
                            tempCol += 1
                            if tempRow == 5 or tempCol == 6:
                                if board[tempRow][tempCol] == val:
                                    checkBoard[tempRow][tempCol] = True
                                    rightColIndices.append(tempCol)
                                    bottomRowIndices.append(tempRow)
                                else:
                                    rightColIndices.append(tempCol-1)
                                    bottomRowIndices.append(tempRow-1)
                                counting = False
                            else:
                                if board[tempRow][tempCol] == val:
                                    checkBoard[tempRow][tempCol] = True
                                else:
                                    counting = False
                                    rightColIndices.append(tempCol-1)
                                    bottomRowIndices.append(tempRow-1)

    #iterate through sets of diagonal streak end points
    if len(leftColIndices) != len(rightColIndices) and len(leftColIndices) != len(topRowIndices) and len(leftColIndices) != len(bottomRowIndices):
        print "ERROR: upper right diagonal index lists not same size"
    else:
        for i in range(len(leftColIndices)):
            leftIndex = leftColIndices[i]
            rightIndex = rightColIndices[i]
            topIndex = topRowIndices[i]
            bottomIndex = bottomRowIndices[i]

            if leftIndex == rightIndex:
                continue
            else:
                streakLength = rightIndex - leftIndex + 1
                leftFreeSpots = 0
                rightFreeSpots = 0

                #check free spots up and to the left
                if leftIndex == 0:
                    pass
                elif leftIndex == 1:
                    if topIndex != 0:
                        if board[topIndex-1][leftIndex-1] == ' ':
                            leftFreeSpots += 1
                else:
                    if topIndex != 1 and topIndex != 0:
                        if board[topIndex-1][leftIndex-1] == ' ' and board[topIndex-2][leftIndex-2] in (' ', val):
                            leftFreeSpots += 2
                        elif board[topIndex-1][leftIndex-1] == ' ':
                            leftFreeSpots += 1
                    elif bottomIndex != 0:
                        #bottom index = 4
                        if board[topIndex-1][leftIndex-1] == ' ':
                            leftFreeSpots += 1

                #check free spots down and to the right
                if rightIndex == 6:
                    pass
                elif rightIndex == 5:
                    if bottomIndex != 5:
                        if board[bottomIndex+1][rightIndex+1] == ' ':
                            rightFreeSpots += 1
                else:
                    if bottomIndex != 4 and bottomIndex != 5:
                        if board[bottomIndex+1][rightIndex+1] == ' ' and board[bottomIndex+2][rightIndex+2] in (' ', val):
                            rightFreeSpots += 2
                        elif board[bottomIndex+1][rightIndex+1] == ' ':
                            rightFreeSpots += 1
                    elif bottomIndex != 5:
                        if board[topIndex+1][rightIndex+1] == ' ':
                            rightFreeSpots += 1

                if (streakLength + leftFreeSpots + rightFreeSpots) >= 4:
                    retDict[streakLength] += 1
    return retDict

# calculates the utility of a given board state
def utility(board):
    print board
    if activePlayer == 0:
        valToCheck = "X"
    else:
        valToCheck = "O"

    twoStreakMult = 1
    threeStreakMult = 3
    fourStreakMult = 8

    #key is number of values in streak, value is the number of streaks for that key
    rowScore = {2:0, 3:0, 4:0}
    colScore = {2:0, 3:0, 4:0}
    upRightDiagScore = {2:0, 3:0, 4:0}
    upLeftDiagScore = {2:0, 3:0, 4:0}

    #check for vertical matches
    for col in range(7):
        count = checkColumn(board, valToCheck, col)     #returns [0-4]
        if count > 1:
            colScore[count] += 1


    #check for horizontal matches
    for row in range(6):
        streakCountDict = checkRow(board, valToCheck, row)
        rowScore[2] += streakCountDict[2]
        rowScore[3] += streakCountDict[3]
        rowScore[4] += streakCountDict[4]

    streakCountDict = checkUpperRightDiagonals(board, valToCheck)
    upRightDiagScore[2] += streakCountDict[2]
    upRightDiagScore[3] += streakCountDict[3]
    upRightDiagScore[4] += streakCountDict[4]

    streakCountDict = checkUpperLeftDiagonals(board, valToCheck)
    upLeftDiagScore[2] += streakCountDict[2]
    upLeftDiagScore[3] += streakCountDict[3]
    upLeftDiagScore[4] += streakCountDict[4]

    print "\n==========================\nREPORT FOR %s VALUES\n==========================\n" % valToCheck
    print "Valid vertical streaks:\n2:%d\n3:%d\n4:%d\n" % (colScore[2], colScore[3], colScore[4])
    print "Valid horizontal streaks:\n2:%d\n3:%d\n4:%d\n" % (rowScore[2],rowScore[3],rowScore[4])
    print "Valid northeast streaks:\n2:%d\n3:%d\n4:%d\n" % (upRightDiagScore[2], upRightDiagScore[3], upRightDiagScore[4])
    print "Valid northwest streaks:\n2:%d\n3:%d\n4:%d\n" % (upLeftDiagScore[2], upLeftDiagScore[3], upLeftDiagScore[4])

    totalScore = 0
    totalScore += (twoStreakMult * (rowScore[2] + colScore[2] + upRightDiagScore[2] + upLeftDiagScore[2]))
    totalScore += (threeStreakMult * (rowScore[3] + colScore[3] + upRightDiagScore[2] + upLeftDiagScore[2]))
    totalScore += (fourStreakMult * (rowScore[4] + colScore[4] + upRightDiagScore[2] + upLeftDiagScore[2]))
    print "Total score for %s is %d\n" % (valToCheck, totalScore)
    return totalScore

def run_AI(board, ID):
    global activePlayer
    activePlayer = ID
    v = alpha_beta_search(board)
    return str(v)
