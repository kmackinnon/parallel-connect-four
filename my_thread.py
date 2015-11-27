import minimaxAIParallel as ai
import minimaxCommon as mmUtil

def find_min(board,activePlayer,alpha,beta,depth,a):

	return (a, ai.min_value(mmUtil.make_move(board,a,activePlayer), alpha, beta, depth+1))
