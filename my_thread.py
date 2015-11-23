import minimaxAI as ai
	
def find_min(board,activePlayer,alpha,beta,depth,a):

	return ai.min_value(ai.make_move(board,a,activePlayer), alpha, beta, depth+1)
