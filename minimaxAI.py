import sys
import copy
import time
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
		vMin = min_value(make_move(board,a), alpha, beta, depth+1)
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
	if terminal_test(board) or timeCheck() or depth > maxDepth:
		return utility(board)
	v = float('-inf')
	for a in get_moves(board):
		v = max(v, min_value(make_move(board,a), alpha, beta, depth+1))
		if v >= beta:
			return v
		alpha = max(alpha,v)
	return v

def min_value(board, alpha, beta, depth):
	if terminal_test(board) or timeCheck() or depth > maxDepth:
		return utility(board)
	v = float('inf')
	for a in get_moves(board):
		v = min(v, max_value(make_move(board,a), alpha, beta, depth+1))
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

def make_move(board, col):
	tempBoard = copy.deepcopy(board)
	if activePlayer == 0:
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

# checks if board is full or if a player has won
def terminal_test(board):
	# check if board is full
	count = 0
	for y in range(7):
		if board[0][y] == "X" or board[0][y] == "O":
			count = count+1
	if (count==7):
		return True
	# TODO check if player has won
	return False

def timeCheck():
	endTime = time.clock()
	if (endTime - startTime) >= maxTime:
		print "AI OUT OF TIME"
		return True
	else:
		return False

def evaluateBoard(board, player):
    global activePlayer
    activePlayer = player
    return utility(board)

def checkColumn(board, val, col):
    #only returns a count if there is an available slot above the streak of values
    
    #start from the botton and decrement counter
    counting = False
    count = 0
    for row in range(5, 0, -1):
        if board[row][col] == val:
            counting = True
            count += 1
        elif counting:
            counting = False
            if board[row][col] == " ":
                #if empty spot above, nothing else in this column
                break
            else:
                #opponent value above streak, so dont want to include the count cause you cant do anything with it
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
            #print "At (%d,%d), value is '%s', compared to checking value '%s'" % (row,col,board[row][col], val)
            if not leftSet:
                leftSet = True
                leftIndices.append(col)
        else:
            if leftSet and col != 0:
                rightIndices.append(col-1)
                leftSet = False     #set to false to keep searching for more streaks
        if col == 6 and leftSet:
            rightIndices.append(col)
    
    #check each pair of indices to evaluate the score
    if len(leftIndices) != len(rightIndices):
        print "ROW CHECK ERROR"
        print "Left:" + str(leftIndices)
        print "Right:" + str(rightIndices)
    else:
        for i in range(len(leftIndices)):
            leftSpotsFree = 0
            rightSpotsFree = 0
            leftIndex = leftIndices[i]
            rightIndex = rightIndices[i]
            
            streakLength = rightIndex - leftIndex + 1
            
            if streakLength < 2:
                continue
        
            if leftIndex == 0:
                pass
            elif leftIndex == 1:
                if board[row][leftIndex-1] == " ":
                    leftSpotsFree += 1
            else:
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
                print board
                print "current index:%d, val to check:'%s'" % (i, val)
                print "Left:" + str(leftIndices)
                print "Right:" + str(rightIndices)
                retDict[streakLength] += 1
                print "Row %d has a streak of %d" % (row, streakLength)
    return retDict


    
# calculates the utility of a given board state
def utility(board):
    
    verticalCheckBoard = [[False for x in range(7)] for y in range(6)]
    horizontalCheckBoard = [[False for x in range(7)] for y in range(6)]
    
    if activePlayer == 0:
        valToCheck = "X"
    else:
        valToCheck = "O"
    print board
    #key is number of values in streak, value is the number of streaks for that key
    rowScore = {2:0, 3:0, 4:0}
    colScore = {2:0, 3:0, 4:0}
    
    #check for vertical matches
    for col in range(7):
        count = checkColumn(board, valToCheck, col)     #returns [0-4]
        if count > 1:
            colScore[count] += 1
            print "Count at column " + str(col) + " is " + str(count)
    
    #check for horizontal matches
    for row in range(6):
        streakCountDict = checkRow(board, valToCheck, row)
        rowScore[2] += streakCountDict[2]
        rowScore[3] += streakCountDict[3]
        rowScore[4] += streakCountDict[4]
    print "\n\n%s has:\nValid 2 streak rows:%d\nValid 3 streak rows:%d\nValid 4 streak rows:%d" % (valToCheck,rowScore[2], rowScore[3], rowScore[4])
    print "\n%s has:\nValid 2 streak cols:%d\nValid 3 streak cols:%d\nValid 4 streak cols:%d" % (valToCheck,colScore[2], colScore[3], colScore[4])
    
    totalScore = 0
    totalScore += (1 * (rowScore[2] + colScore[2]))
    totalScore += (4 * (rowScore[3] + colScore[3]))
    totalScore += (10 * (rowScore[4] + colScore[4]))
        
    return totalScore
    
    '''for x in range(6):
		for y in range(7):
			if board[x][y] == valToCheck:
				if x != 0 and x != 5 and y != 0 and y != 6:
					if board[x][y+1] == valToCheck:
						score = score + 5
					if board[x][y-1] == valToCheck:
						score = score + 5
					if board[x+1][y] == valToCheck:
						score = score + 5
					if board[x-1][y] == valToCheck:
						score = score + 5
					if board[x+1][y+1] == valToCheck:
						score = score + 3
					if board[x+1][y-1] == valToCheck:
						score = score + 3
					if board[x-1][y+1] == valToCheck:
						score = score + 3
					if board[x-1][y-1] == valToCheck:
						score = score + 3

					if board[x][y+1] != valToCheck:
						score = score - 10
					if board[x][y-1] != valToCheck:
						score = score - 10
					if board[x+1][y] != valToCheck:
						score = score - 10
					if board[x-1][y] != valToCheck:
						score = score - 10
					if board[x+1][y+1] != valToCheck:
						score = score - 8
					if board[x+1][y-1] != valToCheck:
						score = score - 8
					if board[x-1][y+1] != valToCheck:
						score = score - 8
					if board[x-1][y-1] != valToCheck:
						score = score - 8
	return score
    '''

def run_AI(board, ID):
	global activePlayer
	activePlayer = ID
	v = alpha_beta_search(board)
	return str(v)
