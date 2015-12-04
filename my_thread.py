import minimaxAIParallel as ai
import minimaxCommon as mmUtil

def find_min(board, activePlayer, alpha, beta, depth, mov_cpu):
	print "Data for move " + str(mov_cpu[0]) + ": " + str(mov_cpu)
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

		func = partial(find_min, board, activePlayer, alpha, beta, depth+1)
		v_mins = pool.map_async(func, data)
		pool.close()
		pool.join()
		mov_val = max(v_mins.get(), key=itemgetter(1)) # (move, value)
		return mov_val[::-1]
