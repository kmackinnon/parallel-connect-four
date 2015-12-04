import multiprocessing
import minimaxAIParallel as ai
import minimaxCommon as mmUtil
from functools import partial
from operator import itemgetter

def find_min(board, activePlayer, alpha, beta, depth, mov_cpu):
	print "[" + str(depth) + "] Data for move " + str(mov_cpu[0]) + ": " + str(mov_cpu)
	a = mov_cpu[0]
	numCPU = mov_cpu[1]

	if numCPU == 1:
		return (a, ai.min_value(mmUtil.make_move(board,a,activePlayer), alpha, beta, depth+1))
	else:
		moves = mmUtil.get_moves(board)
		data = []
		for move in moves:
			data.append((move, 1))

		pool = multiprocessing.Pool(processes = numCPU)

		func = partial(find_max, board, activePlayer, alpha, beta, depth+1)
		v_maxs = pool.map_async(func, data)
		pool.close()
		pool.join()
		mov_val = min(v_maxs.get(), key=itemgetter(1)) # (move, value)
		return mov_val

def find_max(board, activePlayer, alpha, beta, depth, mov_cpu):
	print "[" + str(depth) + "]Data for move " + str(mov_cpu[0]) + ": " + str(mov_cpu)
	a = mov_cpu[0]
	if activePlayer == 1:
		opponentPlayer = 0
	else:
		opponentPlayer = 1
	return (a, ai.max_value(mmUtil.make_move(board,a,opponentPlayer), alpha, beta, depth+1))
