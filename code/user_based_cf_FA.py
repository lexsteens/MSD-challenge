from evaluator import evaluator
from dataset import dataset
from user_distance import user_distance
import time
import json
import math

global_debug_info = {}

class user_based_cf_recommender_FA:
	def __init__(self, dataset, distances , A=0.5, Q=3):
		self.dataset = dataset
		self.distances = distances
		self.A = A
		self.Q = Q
	
	def recommend(self, user):
		user_songs = self.dataset.user_item_matrix['binary'][user]
		
		user_to_debug = 'c34670d9c1718361feb93068a853cead3c95b76a'

		user_name = self.dataset.index2user[user]
		if user_name == user_to_debug:
			debug_info = {
				self.dataset.index2user[user]: dict([(self.dataset.index2item[item], value) for item, value in self.dataset.user_item_matrix['count'][user].items()])
				, 'similar_users': {}
				}
		
		ranking = {}
		for similar_user in self.dataset.user_item_matrix['binary']:
			if similar_user != user:
				similar_user_songs = self.dataset.user_item_matrix['binary'][similar_user]
				
				w = float(len(set(similar_user_songs) & set(user_songs)))
				if w > 0:
					l1 = len(user_songs)
					l2 = len(similar_user_songs)
					dist = w / (math.pow(l1, self.A) * (math.pow(l2, (1.0 - self.A))))
				else:
					continue
					
				if user == 37244 and similar_user == 98400:
					print user_songs
					print similar_user_songs
					print self.A, l1, math.pow(l1, self.A), l2, math.pow(l2, self.A), w, dist
				
				if user_name == user_to_debug:
					similar_user_name = self.dataset.index2user[similar_user]
					debug_info['similar_users'][similar_user_name] = {}
					debug_info['similar_users'][similar_user_name]['dist'] = dist
					debug_info['similar_users'][similar_user_name]['songs'] = {}
				
				for item in similar_user_songs:
					
					if user_name == user_to_debug:
						item_id = self.dataset.index2item[item]
						debug_info['similar_users'][similar_user_name]['songs'][item_id] = self.dataset.user_item_matrix['count'][similar_user][item]
				
					if item not in user_songs:
						if  item not in ranking:
							ranking[item] = 0
						ranking[item] += pow(dist, self.Q)
		
		rec = [(tuple[0], tuple[1], idx) for idx, tuple in enumerate(sorted(ranking.items(), key=lambda x: x[1], reverse=True))]
		
		if user_name == user_to_debug:
			debug_info['ranking'] = [self.dataset.index2item[item] + '(' + str(score) + ')[' + str(rank) + ']' for item, score, rank in rec]
			global_debug_info['recommender'] = debug_info

		return rec
		

		
if __name__ == '__main__':
	dataset_ts = dataset('kaggle_visible_evaluation_triplets_ts.txt')
	user_dist = user_distance(dataset_ts, 'cosine', 'count')
	recommender = user_based_cf_recommender_FA(dataset_ts, user_dist, A=0.5, Q=3)
	
	dataset_vs = dataset('kaggle_visible_evaluation_triplets_vs.txt')
	evaluator = evaluator(dataset_vs, 500)
	
	# rec = recommender.recommend(65537)
	# for song, dist in rec[:50]:
		# print song, dist
	# evaluator.add_ranking(65537, map(lambda x: x[0], recommender.recommend(65537)))
	# print evaluator.get_MAP()
	
	
	user_index = dataset_ts.user2index['c34670d9c1718361feb93068a853cead3c95b76a']
	print user_index
	rec = recommender.recommend(user_index)
	for song, dist, rank in rec[:5]:
		print dataset_ts.index2item[song], dist, rank
	evaluator.add_ranking(user_index, rec)
	print evaluator.get_MAP()
	
	with open('debug_FA.txt', 'w') as outfile:
		json.dump(global_debug_info, outfile, indent=4)
	
	
	
	
	# users = sorted(dataset_ts.user_item_matrix['binary'].iterkeys())
	# n = len(users)
	
	# sti = time.clock()
	# i = 0
	
	
	# for user in users:
	
		
		# i += 1
		# if i % 100 == 0 and i > 0:
			# cti = time.clock()
			# t = cti - sti
			# print "%d / %d) tot secs: %f (%f / user) %f"%(i, n, t,t/(i+1), evaluator.get_MAP())
	
		# evaluator.add_ranking(user, recommender.recommend(user))
	
	# evaluator.save_details('evaluator_FA.txt')