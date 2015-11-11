import minimaxAI as ai

def gameOver(board, player):
    return verticalWin(board, player) or horizontalWin(board, player) or diagonalWin(board, player)

# test to see if somebody got four consecutive vertical pieces
def verticalWin(board, player):
    val = playerToCheck(player)

    for col in range(7):
        colNum = ai.checkColumn(board, val, col)
        if colNum == 4:
            return True

    return False

# test to see if somebody got four consecutive horizontal pieces
def horizontalWin(board, player):
    val = playerToCheck(player)

    for row in range(6):
        retDict = ai.checkRow(board, val, row)
        if retDict[4] == 1:
            return True

    return False

# test to see if somebody got four diagonal pieces
def diagonalWin(board, player):
    val = playerToCheck(player)

    upperRightDict = ai.checkUpperRightDiagonals(board, val)
    upperLeftDict = ai.checkUpperLeftDiagonals(board, val)

    return upperRightDict[4] == 1 or upperLeftDict[4] == 1

# we only check for a win on a specific player
def playerToCheck(player):
    if player == 0:
        valToCheck = "X"
    else:
        valToCheck = "O"

    return valToCheck