from evaluator import evaluator
from dataset import dataset
from user_distance import user_distance
import time
import json
import sys
import math



global_debug_info = {}

class user_based_cf_recommender:
	def __init__(self, dataset, distances, Qs, mnn=500):
		self.dataset = dataset
		self.distances = distances
		self.construction = self.distances.construction
		self.method = self.distances.method
		self.Qs = Qs
		self.mnn = mnn
	
	def recommend_user(self, user):
		similar_users = self.distances.nearestNeighboors(user)[:self.mnn]
		
		recs = []
		for q in self.Qs:		
			ranking = {}
			for similar_user, dist in similar_users:
				
				for item in self.dataset.user_item_matrix[self.construction][similar_user]:
					
					if item not in self.dataset.user_item_matrix[self.construction][user]:
						if item not in ranking:
							ranking[item] = 0
						ranking[item] += pow(dist * math.log(self.dataset.user_item_matrix['count'][similar_user][item]), q)
			
			rec = [(tuple[0], tuple[1], idx) for idx, tuple in enumerate(sorted(ranking.items(), key=lambda x: x[1], reverse=True))]
			recs.append(rec)
		
		return recs
		
		

def recommend_users(dataset_ts, dataset_vs, method, construction, alphas=[0.5], Qs=[3], mnn=500):
	print "alphas: ", alphas
	print "Qs: ", Qs
	for alpha in alphas:
		distances = user_distance(dataset_ts, method, construction, alpha)
		
		evaluators = []
		for q in Qs:
			filename = "MAP_ucf2_" + method + "_" + construction + "_alpha=" + str(alpha) + "_mnn=" + str(mnn)+ "_q=" + str(q) + ".txt"
			print filename
			ev = evaluator(dataset_vs, 500, filename)
			evaluators.append(ev)
		
		recommender = user_based_cf_recommender(dataset_ts, distances, Qs=Qs, mnn=mnn)
		
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

	ds_name = sys.argv[1]
	construction = sys.argv[2]
	method = sys.argv[3]

	dataset_ts = dataset(ds_name + '_ts.txt', user_item_constructions=[construction, 'count'])	
	dataset_vs = dataset(ds_name + '_vs.txt', user_item_constructions=['count'], item_user_constructions=[])
	recommend_users(dataset_ts, dataset_vs, method, construction, alphas=[float(val)/100 for val in range(0, 105, 5)], Qs=range(2, 6), mnn=50)
	

	
	

	
	
	# user_index = dataset_ts.user2index['c34670d9c1718361feb93068a853cead3c95b76a']
	# print user_index
	# rec = recommender.recommend(user_index)
	# for song, dist, rank in rec[:5]:
		# print dataset_ts.index2item[song], dist, rank
	# evaluator.add_ranking(user_index, rec)
	# print evaluator.get_MAP()
	
	# with open('debug.txt', 'w') as outfile:
		# json.dump(global_debug_info, outfile, indent=4)
	
	
	
	
