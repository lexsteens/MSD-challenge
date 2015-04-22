from evaluator import evaluator

class user_based_cf_recommender:
	def __init__(self, user_item_matrix, evaluator):
		self.user_item_matrix = user_item_matrix
		self.evaluator = evaluator
	
	def predict:
		
	
if __name__ == '__main__':
	print 'loading evaluation triplets...'
	f = open('kaggle_visible_evaluation_triplets_ts.txt', 'r')
	user_item_matrix = {}
	for line in f:
		user, song, count = line.strip().split('\t')
		if user in user_item_matrix:
			user_item_matrix[user][song] = count
		else:
			user_item_matrix[user] = {}
			user_item_matrix[user][song] = count
	f.close()
	print "done."
	
	recommender = user_based_cf_recommender(user_item_matrix, evaluator(500))