

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
            leftPlayableSpotsFree = 0
            rightSpotsFree = 0
            rightPlayableSpotsFree = 0
            leftIndex = leftIndices[i]
            rightIndex = rightIndices[i]

            #add 1 to account for zero indexing
            streakLength = rightIndex - leftIndex + 1

            if streakLength < 2:
                #dont care about single value
                continue
            
            if streakLength >= 4:
                retDict[4] += 1
                continue

            if leftIndex == 0:
                #obviously no left spots available
                pass
            elif leftIndex == 1:
                if board[row][leftIndex-1] == " ":
                    leftSpotsFree += 1
                    if row == 5 or board[row+1][leftIndex-1] != ' ':
                        leftPlayableSpotsFree += 1
            else:
                #need at most 2 empty spots, since streaks < 2 haven't gotten this far
                if board[row][leftIndex-2] == " " and board[row][leftIndex-1] == " ":
                    leftSpotsFree += 2
                    if row == 5 or (board[row+1][leftIndex-2] != ' ' and board[row+1][leftIndex-1] != ' '):
                        leftPlayableSpotsFree += 2
                    elif board[row+1][leftIndex-1] != ' ':
                        leftPlayableSpotsFree += 1
                elif board[row][leftIndex-1] == " ":
                    leftSpotsFree += 1
                    if row == 5 or board[row+1][leftIndex-1] != ' ':
                        leftPlayableSpotsFree += 1

            if rightIndex == 6:
                pass
            elif rightIndex == 5:
                if board[row][rightIndex+1] == " ":
                    rightSpotsFree += 1
                    if row == 5 or board[row+1][rightIndex+1] != ' ':
                        rightPlayableSpotsFree += 1
            else:
                if board[row][rightIndex+2] == " " and board[row][rightIndex+1] == " ":
                    rightSpotsFree += 2
                    if row == 5 or (board[row+1][rightIndex+2] != ' ' and board[row+1][rightIndex+1] != ' '):
                        rightPlayableSpotsFree += 2
                    elif board[row+1][rightIndex+1] != ' ':
                        rightPlayableSpotsFree += 1
                elif board[row][rightIndex+1] == " ":
                    rightSpotsFree += 1
                    if row == 5 or board[row+1][rightIndex+1] != ' ':
                        rightPlayableSpotsFree += 1


            if (streakLength + leftSpotsFree + rightSpotsFree) >= 4:
                #increment the number of streakLength streaks
                if streakLength >= 4:
                    streakLength = 4
                
                if leftPlayableSpotsFree != 0 or rightPlayableSpotsFree != 0:
                    retDict[streakLength] += 1

        #check for gaps
        for i in range(len(leftIndices)):
            if i != (len(leftIndices) - 1):
                #not the last element
                leftIndex = leftIndices[i]
                rightIndex = rightIndices[i]
                nextLeftIndex = leftIndices[i+1]
                nextRightIndex = rightIndices[i+1]

                #if X at 2 and 4, gap at index 3 and gapLength == 1 (minus 1 for 0 indexing)
                gapLength = nextLeftIndex - rightIndex - 1
                if gapLength == 1:
                    #gap detected, need to check if it is empty
                    gapIndex = rightIndex + gapLength
                    if board[row][gapIndex] == " " and (row == 5 or board[row+1][gapIndex] != ' '):
                        #valid gap detected
                        leftStreak = rightIndex - leftIndex + 1
                        rightStreak = nextRightIndex - nextLeftIndex + 1
                        streakLength = leftStreak + rightStreak
                        if streakLength >= 4:
                            streakLength = 3
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
        #will hold the length of the streak that the gap is between
        gapCheck = [[0 for x in range(7)] for y in range(6)]

        #check each set of indices, each set represents one diagonal streak
        for i in range(len(leftColIndices)):
            leftIndex = leftColIndices[i]
            rightIndex = rightColIndices[i]
            topIndex = topRowIndices[i]
            bottomIndex = bottomRowIndices[i]


            if leftIndex != rightIndex:
                streakLength = rightIndex - leftIndex + 1

                #check for free spots on either end of the streak
                leftFreeSpots = 0
                leftPlayableFreeSpots = 0
                rightFreeSpots = 0
                rightPlayableFreeSpots = 0

                if streakLength >= 4:
                    retDict[4] += 1
                    continue

                #check free spots down and to the left
                if leftIndex == 0:
                    pass
                elif leftIndex == 1:
                    if bottomIndex != 5:
                        if board[bottomIndex+1][leftIndex-1] in (' ', val):
                            leftFreeSpots += 1
                            try:
                                if board[bottomIndex+2][leftIndex-1] != ' ':
                                    leftPlayableFreeSpots += 1
                            except:
                                pass
                else:
                    #look 2 cells in this direction
                    if bottomIndex != 4 and bottomIndex != 5:
                        if board[bottomIndex+1][leftIndex-1] == ' ' and board[bottomIndex+2][leftIndex-2] == val:
                            #there is a gap, since at least 2 on one side, can assume it goes 2 + gap + 1, so 3 streak
                            
                            try:
                                if board[bottomIndex+2][leftIndex-1] != ' ':
                                    leftPlayableFreeSpots += 1
                                    if gapCheck[bottomIndex+1][leftIndex-1] == 0:
                                        retDict[3] += 1
                                        gapCheck[bottomIndex+1][leftIndex-1] = 3
                                    elif gapCheck[bottomIndex+1][leftIndex-1] < 3:
                                        retDict[gapCheck[bottomIndex+1][leftIndex-1]] -= 1
                                        retDict[3] += 1
                                        gapCheck[bottomIndex+1][leftIndex-1] = 3
                                    continue
                            except IndexError:
                                pass
                            
                        #also consider val a free space when looking 2 cells away, to account for gaps
                        elif board[bottomIndex+1][leftIndex-1] == ' ' and board[bottomIndex+2][leftIndex-2] == ' ':
                            leftFreeSpots += 2
                            if board[bottomIndex+2][leftIndex-1] != ' ':
                                leftPlayableFreeSpots += 1
                                try:
                                    if board[bottomIndex+3][leftIndex-2] != ' ':
                                        leftPlayableFreeSpots += 1
                                except:
                                    if bottomIndex+3 == 5:
                                        leftPlayableFreeSpots += 1
                                        
                        elif board[bottomIndex+1][leftIndex-1] == ' ':
                            leftFreeSpots += 1
                            if board[bottomIndex+2][leftIndex-1] != ' ':
                                leftPlayableFreeSpots += 1
                    elif bottomIndex != 5:
                        #bottom index = 4
                        if board[bottomIndex+1][leftIndex-1] == ' ':
                            leftFreeSpots += 1
                            leftPlayableFreeSpots += 1

                #check free spots up and to the right
                if rightIndex == 6:
                    pass
                elif rightIndex == 5:
                    if topIndex != 0:
                        if board[topIndex-1][rightIndex+1] == ' ':
                            rightFreeSpots += 1
                            try:
                                if board[topIndex][rightIndex+1] != ' ':
                                    rightPlayableFreeSpots += 1
                            except:
                                pass
                else:
                    if topIndex != 1 and topIndex != 0:
                        if board[topIndex-1][rightIndex+1] == ' ' and board[topIndex-2][rightIndex+2] == val:        
                            try:
                                if board[topIndex][rightIndex+1] != ' ':
                                    if gapCheck[topIndex-1][rightIndex+1] == 0:
                                        retDict[3] += 1
                                        gapCheck[topIndex-1][rightIndex+1] = 3
                                    elif gapCheck[topIndex-1][rightIndex+1] < 3:
                                        retDict[gapCheck[topIndex-1][rightIndex+1]] -= 1
                                        retDict[3] += 1
                                        gapCheck[topIndex-1][rightIndex+1] = 3
                                    continue
                            except IndexError:
                                pass
                        elif board[topIndex-1][rightIndex+1] == ' ' and board[topIndex-2][rightIndex+2] == ' ':
                            rightFreeSpots += 2
                            if board[topIndex][rightIndex+1] != ' ':
                                rightPlayableFreeSpots += 1
                                if board[topIndex-1][rightIndex+2] != ' ':
                                    rightPlayableFreeSpots += 1
                        elif board[topIndex-1][rightIndex+1] == ' ':
                            rightFreeSpots += 1
                            if board[topIndex][rightIndex+1] != ' ':
                                rightPlayableFreeSpots += 1
                    elif topIndex != 0:
                        #topIndex = 1
                        if board[topIndex-1][rightIndex+1] == ' ':
                            rightFreeSpots += 1
                            if board[topIndex][rightIndex+1] != ' ':
                                rightPlayableFreeSpots += 1

                if (streakLength + leftFreeSpots + rightFreeSpots) >= 4:
                    #a possible 4 in a row could occur, so increment the number of valid streaks
                    if streakLength >= 4:
                        streakLength = 4
                    
                    if leftPlayableFreeSpots != 0 or rightPlayableFreeSpots != 0:
                        retDict[streakLength] += 1
            else:
                #leftIndex == rightIndex:
                if topIndex > 1 and rightIndex < 4:
                    if board[topIndex-1][rightIndex+1] == ' ' and board[topIndex-2][rightIndex+2] == val:
                        if board[topIndex][rightIndex+1] != ' ':
                            if gapCheck[topIndex-1][rightIndex+1] == 0:
                                gapCheck[topIndex-1][rightIndex+1] = 2
                                retDict[2] += 1
                if bottomIndex < 4 and leftIndex > 1:
                    if board[bottomIndex+1][leftIndex-1] == ' ' and board[bottomIndex+2][leftIndex-2] == val:
                        #there is a gap, check if gap can be filled on next move
                        if board[bottomIndex+2][leftIndex-1] != ' ':
                            if gapCheck[bottomIndex+1][leftIndex-1] == 0:
                                #if no streak set at this gap, set to 2
                                retDict[2] += 1
                                gapCheck[bottomIndex+1][leftIndex-1] = 2
    return retDict

def checkUpperLeftDiagonals(board, val):
    #Basically same algorithm as previous function, just with opposite orientation
    #look there for comments
    checkBoard = [[0 for x in range(7)] for y in range(6)]
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
        gapCheck = [[False for x in range(7)] for y in range(6)]

        for i in range(len(leftColIndices)):
            leftIndex = leftColIndices[i]
            rightIndex = rightColIndices[i]
            topIndex = topRowIndices[i]
            bottomIndex = bottomRowIndices[i]


            if leftIndex != rightIndex:
                streakLength = rightIndex - leftIndex + 1
                leftFreeSpots = 0
                leftPlayableFreeSpots = 0
                rightFreeSpots = 0
                rightPlayableFreeSpots = 0

                if streakLength >= 4:
                    retDict[4] += 1
                    continue

                #check free spots up and to the left
                if leftIndex == 0:
                    pass
                elif leftIndex == 1:
                    if topIndex != 0:
                        if board[topIndex-1][leftIndex-1] == ' ':
                            leftFreeSpots += 1
                            if board[topIndex][leftIndex-1] != ' ':
                                leftPlayableFreeSpots += 1
                else:
                    if topIndex != 1 and topIndex != 0:
                        if board[topIndex-1][leftIndex-1] == ' ' and board[topIndex-2][leftIndex-2] == val:
                            try:
                                if board[topIndex][leftIndex-1] != ' ':
                                    if gapCheck[topIndex-1][leftIndex-1] == 0:
                                        retDict[3] += 1
                                        gapCheck[topIndex-1][leftIndex-1] = 3
                                    elif gapCheck[topIndex-1][leftIndex-1] < 3:
                                        retDict[gapCheck[topIndex-1][leftIndex-1]] -= 1
                                        retDict[3] += 1
                                        gapCheck[topIndex-1][leftIndex-1] = 3
                                    continue
                            except IndexError:
                                pass
                        elif board[topIndex-1][leftIndex-1] == ' ' and board[topIndex-2][leftIndex-2] == ' ':
                            leftFreeSpots += 2
                            if board[topIndex][leftIndex-1] != ' ':
                                leftPlayableFreeSpots += 1
                                if board[topIndex-1][leftIndex-2] != ' ':
                                    leftPlayableFreeSpots += 1
                        elif board[topIndex-1][leftIndex-1] == ' ':
                            leftFreeSpots += 1
                            if board[topIndex][leftIndex-1] != ' ':
                                leftPlayableFreeSpots += 1
                    elif bottomIndex != 0:
                        #bottom index = 4
                        if board[topIndex-1][leftIndex-1] == ' ':
                            leftFreeSpots += 1
                            if board[topIndex][leftIndex-1] != ' ':
                                leftPlayableFreeSpots += 1

                #check free spots down and to the right
                if rightIndex == 6:
                    pass
                elif rightIndex == 5:
                    if bottomIndex != 5:
                        if board[bottomIndex+1][rightIndex+1] == ' ':
                            rightFreeSpots += 1
                            try:
                                if board[bottomIndex+2][rightIndex+1] != ' ':
                                    rightPlayableFreeSpots += 1
                            except:
                                pass
                else:
                    if bottomIndex != 4 and bottomIndex != 5:
                        if board[bottomIndex+1][rightIndex+1] == ' ' and board[bottomIndex+2][rightIndex+2] == val:
                            
                            try:
                                if board[bottomIndex+2][rightIndex+1] != ' ':
                                    if gapCheck[bottomIndex+1][rightIndex+1] == 0:
                                        retDict[3] += 1
                                        gapCheck[bottomIndex+1][rightIndex+1] = 3
                                    elif gapCheck[bottomIndex+1][rightIndex+1] < 3:
                                        retDict[gapCheck[bottomIndex+1][rightIndex+1]] -= 1
                                        retDict[3] += 1
                                        gapCheck[bottomIndex+1][rightIndex+1] = 3
                                    continue
                            except IndexError:
                                pass
                        elif board[bottomIndex+1][rightIndex+1] == ' ' and board[bottomIndex+2][rightIndex+2] == ' ':
                            rightFreeSpots += 2
                            if board[bottomIndex+2][rightIndex+1] != ' ':
                                rightPlayableFreeSpots += 1
                                try:
                                    if board[bottomIndex+3][rightIndex+2] != ' ':
                                        rightPlayableFreeSpots += 1
                                except:
                                    if bottomIndex+3 == 5:
                                        rightPlayableFreeSpots += 1
                                        
                        elif board[bottomIndex+1][rightIndex+1] == ' ':
                            rightFreeSpots += 1
                            if board[bottomIndex+2][rightIndex+1] != ' ':
                                rightPlayableFreeSpots += 1
                    elif bottomIndex != 5:
                        #bottom index = 4
                        if board[topIndex+1][rightIndex+1] == ' ':
                            rightFreeSpots += 1
                            rightPlayableFreeSpots += 1

                if (streakLength + leftFreeSpots + rightFreeSpots) >= 4:
                    if streakLength >= 4:
                        streakLength = 4
                    
                    if leftPlayableFreeSpots != 0 or rightPlayableFreeSpots != 0:
                        retDict[streakLength] += 1
            else:
                if topIndex > 1 and leftIndex > 1:
                    if board[topIndex-1][leftIndex-1] == ' ' and board[topIndex-2][leftIndex-2] == val:
                        if board[topIndex][leftIndex-1] != ' ':
                            if gapCheck[topIndex-1][leftIndex-1] == 0:
                                retDict[2] += 1
                                gapCheck[topIndex-1][leftIndex-1] = 2
                if bottomIndex < 4 and rightIndex < 4:
                    if board[bottomIndex+1][rightIndex+1] == ' ' and board[bottomIndex+2][rightIndex+2] == val:
                        #there is a gap, check if gap can be filled on next move
                        if board[bottomIndex+2][rightIndex+1] != ' ':
                            if gapCheck[bottomIndex+1][rightIndex+1] == 0:
                                retDict[2] += 1
                                gapCheck[bottomIndex+1][rightIndex+1] = 2
    return retDict

def checkVerticalMatches(board, valToCheck, colScore):
    for col in range(7):
        count = checkColumn(board, valToCheck, col)     #returns [0-4]
        if count > 1:
            colScore[count] += 1

def checkHorizontalMatches(board, valToCheck, rowScore):
    for row in range(6):
        streakCountDict = checkRow(board, valToCheck, row)
        rowScore[2] += streakCountDict[2]
        rowScore[3] += streakCountDict[3]
        rowScore[4] += streakCountDict[4]

def checkUpperRightDiagMatches(board, valToCheck, upRightDiagScore):
    streakCountDict = checkUpperRightDiagonals(board, valToCheck)
    upRightDiagScore[2] += streakCountDict[2]
    upRightDiagScore[3] += streakCountDict[3]
    upRightDiagScore[4] += streakCountDict[4]

def checkUpperLeftDiagMatches(board, valToCheck, upLeftDiagScore):
    streakCountDict = checkUpperLeftDiagonals(board, valToCheck)
    upLeftDiagScore[2] += streakCountDict[2]
    upLeftDiagScore[3] += streakCountDict[3]
    upLeftDiagScore[4] += streakCountDict[4]
