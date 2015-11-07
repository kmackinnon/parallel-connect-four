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
		if board[0][y] != 'X ' and board[0][y] != 'O ':
			openSpaces.append(y)
	return openSpaces

def make_move(board, col):
	tempBoard = copy.deepcopy(board)
	if activePlayer == 0:
		valToWrite = "X"
	else:
		valToWrite = "O"
	for i in range(6):
		if tempBoard[i][col] == "  ":
			if i == 5:
				tempBoard[i][col] = valToWrite + " "
				return tempBoard
		else:
			if i != 0:
				tempBoard[i-1][col] = valToWrite + " "
				return tempBoard

# checks if board is full or if a player has won
def terminal_test(board):
	# check if board is full
	count = 0
	for y in range(7):
		if board[0][y] == "X " or board[0][y] == "O ":
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

# calculates the utility of a given board state
def utility(board):
	if activePlayer == 0:
		valToCheck = "X "
	else:
		valToCheck = "O "
	score = 0
	for x in range(6):
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

def run_AI(board, ID):
	global activePlayer
	activePlayer = ID
	v = alpha_beta_search(board)
	return str(v)
