from evaluator import evaluator
from dataset import dataset
from item_distance import item_distance
import time
import json

global_debug_info = {}

class item_based_cf_recommender:
	def __init__(self, dataset, distances, Qs):
		self.dataset = dataset
		self.distances = distances
		self.construction = self.distances.construction
		self.method = self.distances.method
		self.Qs = Qs
	
		print "Storing nearest items..."
		self.nearestItems = {}
		i2u = self.dataset.item_user_matrix[self.construction]
		sti = time.clock()
		i = 0	
		for item in i2u:
			i += 1
			if i % 5000 == 0 and i > 0:
				cti = time.clock()
				t = cti - sti
				print "%d / %d) tot secs: %f (%f / item)"%(i, len(i2u), t,t/(i+1))
		
			self.nearestItems[item] = self.distances.nearestNeighboors(item)
		print "done."
			
	
	def recommend_user(self, user):
		
		recs = []
		for q in self.Qs:		
			scores = {}
			for item in self.dataset.user_item_matrix[self.construction][user]:
				# print self.dataset.index2item[item]

				for similar_item, dist in self.nearestItems[item]:
					# print self.dataset.index2item[item], self.dataset.index2item[similar_item], dist

					if similar_item not in self.dataset.user_item_matrix[self.construction][user]:
						# print self.dataset.index2item[item], self.dataset.index2item[similar_item], dist
						if similar_item not in scores:
							scores[similar_item] = 0
						scores[similar_item] += pow(dist, q)
			
			rec = [(tuple[0], tuple[1], idx) for idx, tuple in enumerate(sorted(scores.items(), key=lambda x: x[1], reverse=True))]
			recs.append(rec)
		
		return recs
		

def recommend_users(dataset_ts, dataset_vs, method, construction, alphas=[0.5], Qs=[3]):
	print "alphas: ", alphas
	print "Qs: ", Qs
	for alpha in alphas:
		distances = item_distance(dataset_ts, method, construction, alpha)
		
		evaluators = []
		for q in Qs:
			filename = "MAP_icf_" + method + "_" + construction + "_alpha=" + str(alpha) + "_q=" + str(q) + ".txt"
			print filename
			ev = evaluator(dataset_vs, 500, filename)
			evaluators.append(ev)
		
		recommender = item_based_cf_recommender(dataset_ts, distances, Qs)
		
		users = sorted(dataset_ts.user_item_matrix[construction].iterkeys())
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
			for idx, rec in enumerate(recs):
				evaluators[idx].add_ranking(user, rec)
			
		for ev in evaluators:
			ev.save_details()
			
		
if __name__ == '__main__':
	dataset_ts = dataset('kaggle_visible_evaluation_triplets_ts.txt', user_item_constructions=['binary'])	
	dataset_vs = dataset('kaggle_visible_evaluation_triplets_vs.txt', user_item_constructions=['count'], item_user_constructions=[])
	recommend_users(dataset_ts, dataset_vs, 'cosine', 'binary', alphas=[float(val)/100 for val in range(0, 110, 5)], Qs=range(1,2))
	

	
	

	
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
	
	
	
	
