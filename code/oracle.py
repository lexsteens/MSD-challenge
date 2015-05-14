from evaluator import evaluator
from dataset import dataset
import time

class oracle_recommender:
	def __init__(self, dataset):
		self.dataset = dataset
	
	def recommend(self, user):
		
		ranking = self.dataset.user_item_matrix['count'][user]
		
		return sorted(ranking.items(), key=lambda x: x[1])
		

		
if __name__ == '__main__':

	

	dataset_vs = dataset('kaggle_visible_evaluation_triplets_vs.txt')
	recommender = oracle_recommender(dataset_vs)
	
	evaluator = evaluator(dataset_vs, 500, 'oracle', subm=True)
	
	
	# print recommender.recommend(65537)
	# evaluator.add_ranking(65537, map(lambda x: x[0], recommender.recommend(65537)))
	# print evaluator.get_MAP()
	
	
	
	users = sorted(dataset_vs.user_item_matrix['binary'].iterkeys())
	n = len(users)
	
	sti = time.clock()
	i = 0
	
	# iterate on users
	for user in users:
	
		# show timing estimate:
		i += 1
		if i % 100 == 0 and i > 0:
			cti = time.clock()
			t = cti - sti
			print "%d / %d) tot secs: %f (%f / user) %d"%(i, n, t,t/(i+1), evaluator.get_MAP())
	
		evaluator.add_ranking(user, map(lambda x: x[0], recommender.recommend(user)))
	