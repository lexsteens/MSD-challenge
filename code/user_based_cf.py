from evaluator import evaluator
from dataset import dataset
from user_distance import user_distance
import time
import json

global_debug_info = {}

class user_based_cf_recommender:
	def __init__(self, dataset, distances, q):
		self.dataset = dataset
		self.distances = distances
		self.q = q
	
	def recommend(self, user):
		similar_users = self.distances.nearestNeighboors(user)
		
		user_to_debug = '04cd8d64e32be6c37a609d4cd548d6947c613829'

		user_name = self.dataset.index2user[user]
		if user_name == user_to_debug:
			debug_info = {
				self.dataset.index2user[user]: dict([(self.dataset.index2item[item], value) for item, value in self.dataset.user_item_matrix['count'][user].items()])
				, 'similar_users': {}
				}
				
				
		ranking = {}
		for similar_user, dist in similar_users:
			
			if user_name == user_to_debug:
				similar_user_name = self.dataset.index2user[similar_user]
				debug_info['similar_users'][similar_user_name] = {}
				debug_info['similar_users'][similar_user_name]['dist'] = dist
				debug_info['similar_users'][similar_user_name]['songs'] = {}
			
			for item in self.dataset.user_item_matrix['count'][similar_user]:
			
				if user_name == user_to_debug:
					item_id = self.dataset.index2item[item]
					debug_info['similar_users'][similar_user_name]['songs'][item_id] = self.dataset.user_item_matrix['count'][similar_user][item]
				
				if item not in self.dataset.user_item_matrix['count'][user]:
					if  item not in ranking:
						ranking[item] = 0
					ranking[item] += pow(1-dist, self.q)
		
		rec = [(tuple[0], tuple[1], idx) for idx, tuple in enumerate(sorted(ranking.items(), key=lambda x: x[1], reverse=True))]
		
		
		if user_name == user_to_debug:
			debug_info['ranking'] = [self.dataset.index2item[item] + '(' + str(score) + ')[' + str(rank) + ']' for item, score, rank in rec]
			global_debug_info['recommender'] = debug_info
		
		return rec
		

		
if __name__ == '__main__':
	dataset_ts = dataset('kaggle_visible_evaluation_triplets_ts.txt')
	dist = user_distance(dataset_ts, 'cosine', 'count')
	recommender = user_based_cf_recommender(dataset_ts, dist, 3)
	
	dataset_vs = dataset('kaggle_visible_evaluation_triplets_vs.txt')
	evaluator = evaluator(dataset_vs, 500)
	
	# rec = recommender.recommend(65537)
	# for song, dist in rec[:50]:
		# print song, dist
	# evaluator.add_ranking(65537, map(lambda x: x[0], recommender.recommend(65537)))
	# print evaluator.get_MAP()
	
	
	# user_index = dataset_ts.user2index['04cd8d64e32be6c37a609d4cd548d6947c613829']
	# print user_index
	# rec = recommender.recommend(user_index)
	# for song, dist, rank in rec[:50]:
		# print dataset_ts.index2item[song], dist, rank
	# evaluator.add_ranking(user_index, rec)
	# print evaluator.get_MAP()
	# evaluator.save_details('evaulator.txt')
	
	# with open('debug.txt', 'w') as outfile:
		# json.dump(global_debug_info, outfile, indent=4)
	
	
	
	
	users = sorted(dataset_ts.user_item_matrix['binary'].iterkeys())
	n = len(users)
	
	sti = time.clock()
	i = 0
	
	
	for user in users:
	
		
		i += 1
		if i % 100 == 0 and i > 0:
			cti = time.clock()
			t = cti - sti
			print "%d / %d) tot secs: %f (%f / user) %f"%(i, n, t,t/(i+1), evaluator.get_MAP())
	
		evaluator.add_ranking(user, recommender.recommend(user))
	
	evaluator.save_details('evaluator.txt')