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
	dataset = dataset('kaggle_visible_evaluation_triplets_ts.txt')
	dist = user_distance(dataset, 'cosine', 'count')
	evaluator = evaluator(500)
	
	recommender = user_based_cf_recommender(dataset, dist, 3)
	# evaluator.add_ranking(65537, map(lambda x: x[0], recommender.recommend(65537)))
	# print evaluator.get_MAP()
	
	
	
	users = sorted(dataset.user_item_matrix['binary'].iterkeys())
	n = len(users)
	
	sti = time.clock()
	i = 0
	
	# iterate on users
	for user in users:
	
		# show timing estimate:
		i += 1
		if i % 100 == 00:
			cti = time.clock()
			t = cti - sti
			print "%d / %d) tot secs: %f (%f / user)"%(i, n, t,t/(i+1))
	
		recommender.recommend(user)