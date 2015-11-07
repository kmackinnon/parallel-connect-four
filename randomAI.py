import sys
from random import randint

def run_AI(board, ID):
	openCols = get_moves(board)

	length = len(openCols)
	if length==0:
		return "k"

	col = randint(0,length-1)

	return str(openCols[col])

def get_moves(board):
	openSpaces = []
	for y in range(7):
		if board[0][y] != 'X ' and board[0][y] != 'O ':
			openSpaces.append(y)
	return openSpaces
