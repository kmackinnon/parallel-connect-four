import sys
import time
import minimaxCommon as mmUtil
import multiprocessing
from functools import partial
from gameover import gameOver
from operator import itemgetter
import my_thread as t

activePlayer = -1
opponentPlayer = -1
maxTime = 15
startTime = 0
maxDepth = 8

# returns an action
def alpha_beta_search(board):
    print "[INFO] PARALLEL"
    global startTime
    startTime = time.clock()
    v = max_value_first(board, float('-inf'), float('inf'), 0)
    return v[1]

# returns a utility value
def max_value_first(board, alpha, beta, depth):
    v = float('-inf')
    moves = mmUtil.get_moves(board)
    
    pool = multiprocessing.Pool()
    func = partial(t.find_min, board, activePlayer, alpha, beta, depth)
    v_mins = pool.map_async(func, moves)
    pool.close()
    pool.join()

    mov_val = max(v_mins.get(), key=itemgetter(1)) # (move, value)

    print v_mins.get()
    print mov_val

    return mov_val[::-1]  # (value, move)

# returns a utility value
def max_value(board, alpha, beta, depth):
    if mmUtil.terminal_test(board, opponentPlayer, depth, startTime, maxTime, maxDepth):
        return mmUtil.utility(board, activePlayer)
    v = float('-inf')
    for a in mmUtil.get_moves(board):
        v = max(v, min_value(mmUtil.make_move(board,a,activePlayer), alpha, beta, depth+1))
        if v >= beta:
            return v
        alpha = max(alpha,v)
    return v

def min_value(board, alpha, beta, depth):
    if mmUtil.terminal_test(board, activePlayer, depth, startTime, maxTime, maxDepth):
        return mmUtil.utility(board, activePlayer)
    v = float('inf')
    for a in mmUtil.get_moves(board):
        v = min(v, max_value(mmUtil.make_move(board,a,opponentPlayer), alpha, beta, depth+1))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v

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
