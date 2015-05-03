from evaluator import evaluator
from dataset import dataset
from user_distance import user_distance
import time
import json

global_debug_info = {}

class user_based_cf_recommender:
	def __init__(self, dataset, distances, Q=3):
		self.dataset = dataset
		self.distances = distances
		self.Q = Q
	
	def recommend(self, user):
		similar_users = self.distances.nearestNeighboors(user)
		
		user_to_debug = 'c34670d9c1718361feb93068a853cead3c95b76a'

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
			
			for item in self.dataset.user_item_matrix['binary'][similar_user]:
			
				if user_name == user_to_debug:
					item_id = self.dataset.index2item[item]
					debug_info['similar_users'][similar_user_name]['songs'][item_id] = self.dataset.user_item_matrix['count'][similar_user][item]
				
				if item not in self.dataset.user_item_matrix['binary'][user]:
					if  item not in ranking:
						ranking[item] = 0
					ranking[item] += pow(dist, self.Q)
		
		rec = [(tuple[0], tuple[1], idx) for idx, tuple in enumerate(sorted(ranking.items(), key=lambda x: x[1], reverse=True))]
		
		
		if user_name == user_to_debug:
			debug_info['ranking'] = [self.dataset.index2item[item] + '(' + str(score) + ')[' + str(rank) + ']' for item, score, rank in rec]
			global_debug_info['recommender'] = debug_info
		
		return rec
		

def compute(dist_type):		
	dist = user_distance(dataset_ts, dist_type, 'binary')
	recommender = user_based_cf_recommender(dataset_ts, dist, 3)
	ev = evaluator(dataset_vs, 500)
	
	users = sorted(dataset_ts.user_item_matrix['binary'].iterkeys())
	n = len(users)
	
	sti = time.clock()
	i = 0	
	for user in users:		
		i += 1
		if i % 100 == 0 and i > 0:
			cti = time.clock()
			t = cti - sti
			print "%d / %d) tot secs: %f (%f / user) %f"%(i, n, t,t/(i+1), ev.get_MAP())
	
		ev.add_ranking(user, recommender.recommend(user))
	
	ev.save_details('evaluator_' + dist_type + '.txt')
		
if __name__ == '__main__':
	dataset_ts = dataset('kaggle_visible_evaluation_triplets_ts.txt')	
	dataset_vs = dataset('kaggle_visible_evaluation_triplets_vs.txt')
	compute('cosine')
	compute('cosine2')
	

	
	

	
	
	# user_index = dataset_ts.user2index['c34670d9c1718361feb93068a853cead3c95b76a']
	# print user_index
	# rec = recommender.recommend(user_index)
	# for song, dist, rank in rec[:5]:
		# print dataset_ts.index2item[song], dist, rank
	# evaluator.add_ranking(user_index, rec)
	# print evaluator.get_MAP()
	
	# with open('debug.txt', 'w') as outfile:
		# json.dump(global_debug_info, outfile, indent=4)
	
	
	
	
