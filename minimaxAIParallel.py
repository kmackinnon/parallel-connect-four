import sys
import time
import minimaxCommon as mmUtil
import multiprocessing
import my_thread as t
import MyPool as p
from functools import partial
from operator import itemgetter

activePlayer = -1
opponentPlayer = -1
maxTime = 20
startTime = 0
maxDepth = 8
numCPU = 0

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
    
    # Get number of extra processors after first level
    num_extra = numCPU - len(moves)
    # Ensure num_extra is positive
    if num_extra < 0:
        num_extra = 0

    pool = p.MyPool(numCPU - num_extra)
    func = partial(t.find_min, board, activePlayer, alpha, beta, depth)

    # Make array of tuples for each node of tree at the next depth
    # each tuple: (move, # of moves available)
    next_nodes = []
    for move in moves:
        temp_board = mmUtil.make_move(board, move, activePlayer)
        num_next = mmUtil.get_moves(temp_board)
        next_nodes.append((move, len(num_next)))

    # Sort by decreasing number of moves available
    sorted(next_nodes, key=itemgetter(1), reverse=True)

    # Create data array for number of processors allocated for each move
    data = []

    # Calculate the base number of extra processors that each move will use
    base = num_extra/len(moves)

    # For each tuple add the base number of extra processors to the default amount (1)
    for node in next_nodes:
        data.append((node[0], 1+base))

    # Allocate remaining processor with moves that have the highest branching factor
    for i in range((num_extra % len(moves))):
        node = data[i]
        data[i] = (node[0], node[1]+1)

    v_mins = pool.map_async(func, data)
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
    global numCPU
    activePlayer = ID
    if activePlayer == 0:
        opponentPlayer = 1
    else:
        opponentPlayer = 0
    numCPU = multiprocessing.cpu_count()
    v = alpha_beta_search(board)
    return str(v)
