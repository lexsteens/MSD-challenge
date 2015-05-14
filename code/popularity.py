from evaluator import evaluator
from dataset import dataset
from item_distance import item_distance
import time
import json
import sys



global_debug_info = {}

class popularity_recommender:
	def __init__(self, dataset):
		self.dataset = dataset
		self.u2i = self.dataset.user_item_matrix[self.dataset.user_item_constructions[0]]
	
		print "Ranking popularities..."
		popularity = {}
		i2u = self.dataset.item_user_matrix[self.dataset.item_user_constructions[0]]
		for item in i2u:
			popularity[item] = len(i2u[item])
		print popularity.items()[:5]
		self.popularity_ranked = sorted(popularity.items(), key=lambda x: x[1], reverse=True)
		print self.popularity_ranked[:5]
		print "Done."
			
	
	def recommend_user(self, user):
		
		scores = {}
		i = 0
		for item, popularity in self.popularity_ranked:
			if item not in self.u2i:
				i += 1
				if i > 500:
					break
				scores[item] = popularity
		
		recs = []
		rec = [(tuple[0], tuple[1], idx) for idx, tuple in enumerate(sorted(scores.items(), key=lambda x: x[1], reverse=True))]
		recs.append(rec)
		
		return recs
		
		

def recommend_users(dataset_ts, dataset_vs, subm=False):
	
	filename = "MAP_popularity.txt"
	ev = evaluator(dataset_vs, 500, filename, subm=subm)
	
	recommender = popularity_recommender(dataset_ts)
	
	users = sorted(dataset_ts.user_item_matrix[dataset_ts.user_item_constructions[0]].iterkeys())
	n = len(users)
	
	sti = time.clock()
	i = 0	
	for user in users:		
		i += 1
		if i % 100 == 0 and i > 0:
			cti = time.clock()
			t = cti - sti
			print "%d / %d) tot secs: %f (%f / user) %f"%(i, n, t,t/(i+1), ev.get_MAP())
	
		recs = recommender.recommend_user(user)
		ev.add_ranking(user, recs[0])
		

	ev.save_details()
			
		
if __name__ == '__main__':

	ds_name = sys.argv[1]

	dataset_ts = dataset(ds_name + '_ts.txt', user_item_constructions=['binary'], item_user_constructions=['binary'])	
	dataset_vs = dataset(ds_name + '_vs.txt', user_item_constructions=['count'], item_user_constructions=[])
	recommend_users(dataset_ts, dataset_vs, subm=True)
	

	
	

	
	# distances = item_distance(dataset_ts, 'cosine', 'binary')
	# recommender = item_based_cf_recommender(dataset_ts, distances, [1])
	# ev = evaluator(dataset_vs, 500, 'ev.txt')
	# user_index = dataset_ts.user2index['0093ea2ad5eebbfe7635a70909b7988d1b340a5a']
	# print user_index
	# rec = recommender.recommend_user(user_index)
	# for song, dist, rank in rec[0][:5]:
		# print dataset_ts.index2item[song], dist, rank
	# ev.add_ranking(user_index, rec[0])
	# print ev.get_MAP()
	
	# with open('debug.txt', 'w') as outfile:
		# json.dump(global_debug_info, outfile, indent=4)
	
	
	
	
