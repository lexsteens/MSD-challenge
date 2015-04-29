from evaluator import evaluator
from dataset import dataset
from user_distance import user_distance
import time

class user_based_cf_recommender:
	def __init__(self, dataset, distances, q):
		self.dataset = dataset
		self.distances = distances
		self.q = q
	
	def recommend(self, user):
		similar_users = self.distances.nearestNeighboors(user)
		
		ranking = {}
		for user, dist in similar_users:
			for item in self.dataset.user_item_matrix['count'][user]:
				if item not in ranking:
					ranking[item] = 0
				ranking[item] += pow(1-dist, self.q)
		
		return sorted(ranking.items(), key=lambda x: x[1])
		

		
if __name__ == '__main__':
	dataset_ts = dataset('kaggle_visible_evaluation_triplets_ts.txt')
	dist = user_distance(dataset_ts, 'cosine', 'count')
	recommender = user_based_cf_recommender(dataset_ts, dist, 3)
	
	dataset_vs = dataset('kaggle_visible_evaluation_triplets_vs.txt')
	evaluator = evaluator(dataset_vs, 500)
	
	# evaluator.add_ranking(65537, map(lambda x: x[0], recommender.recommend(65537)))
	# print evaluator.get_MAP()
	
	
	
	users = sorted(dataset_ts.user_item_matrix['binary'].iterkeys())
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
	
		evaluator.add_ranking(user, recommender.recommend(user))
	