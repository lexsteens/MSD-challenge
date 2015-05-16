from evaluator import evaluator
from dataset import dataset
from item_distance import item_distance
import time
import json
import sys



global_debug_info = {}

class item_based_cf_recommender:
	def __init__(self, dataset, distances, Qs, mnn):
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
		
			self.nearestItems[item] = self.distances.nearestNeighboors(item)[:mnn]
		print "done."
			
	
	def recommend_user(self, user):
		
		scores = []
		for idx, q in enumerate(self.Qs):
			scores.append({})
		
		for item in self.dataset.user_item_matrix[self.construction][user]:
			# print self.dataset.index2item[item]

			for similar_item, dist in self.nearestItems[item]:
				# print self.dataset.index2item[item], self.dataset.index2item[similar_item], dist

				if similar_item not in self.dataset.user_item_matrix[self.construction][user]:
					# print self.dataset.index2item[item], self.dataset.index2item[similar_item], dist
					for idx, q in enumerate(self.Qs):
						if similar_item not in scores[idx]:
							scores[idx][similar_item] = 0
						scores[idx][similar_item] += pow(dist, q)
		
		recs = []
		for idx, q in enumerate(self.Qs):
			rec = [(tuple[0], tuple[1], idx) for idx, tuple in enumerate(sorted(scores[idx].items(), key=lambda x: x[1], reverse=True))]
			recs.append(rec)
		
		return recs
		
		

def recommend_users(dataset_ts, dataset_vs, method, construction, alphas=[0.5], Qs=[1], mnn=500, subm=False):
	print "alphas: ", alphas
	print "Qs: ", Qs
	for alpha in alphas:
		distances = item_distance(dataset_ts, method, construction, alpha)
		
		evaluators = []
		for q in Qs:
			filename = "MAP_icf_" + method + "_" + construction + "_alpha=" + str(alpha) + "_mnn=" + str(mnn) + "_q=" + str(q) + ".txt"
			print filename
			ev = evaluator(dataset_vs, 500, filename, subm=subm)
			evaluators.append(ev)
		
		recommender = item_based_cf_recommender(dataset_ts, distances, Qs=Qs, mnn=mnn)
		
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
	mnn = int(sys.argv[4])

	dataset_ts = dataset(ds_name + '_ts.txt', user_item_constructions=[construction], item_user_constructions=[construction])	
	dataset_vs = dataset(ds_name + '_vs.txt', user_item_constructions=['count'], item_user_constructions=[])
	recommend_users(dataset_ts, dataset_vs, method, construction, alphas=[float(val)/100 for val in range(0, 105, 5)], Qs=range(1,6), mnn=mnn)
	# recommend_users(dataset_ts, dataset_vs, method, construction, alphas=[0.8], Qs=range(1,2), mnn=50, subm=True)
	

	
	

	
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
	
	
	
	
