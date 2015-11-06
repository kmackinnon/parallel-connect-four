import sys
from random import randint

def runAI(board, ID):
	openCols = getMoves(board)

	length = len(openCols)
	if length==0:
		return "k"

	col = randint(0,length-1)
	print "AI moves: "
	print openCols

	return str(openCols[col])

def getMoves(board):
	openSpaces = []
	for y in range(7):
		if board[0][y] != 'X ' and board[0][y] != 'O ':
			openSpaces.append(y)
	return openSpaces
