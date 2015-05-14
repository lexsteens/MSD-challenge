from evaluator import evaluator
from dataset import dataset
from item_distance import item_distance
import time
import json
import sys



global_debug_info = {}

class from_file_recommender:
	def __init__(self, filename):
			self.filename = filename
			self.infile = open(filename, 'r')
	
	
	
	
	def recommend_user(self, user):
		
		line = self.infile.readline()
		user_from_file, recs_from_file = line.split('\t')
		
		user_from_file = int(user_from_file.strip())
		if user_from_file != user:
			raise Exception('Expecting user ' + str(user) + ' but got user ' + str(user_from_file) + ' in file ' + self.filename)
		
		recs = []
		for rec_from_file in recs_from_file.split(' '):
			if len(rec_from_file.strip()) != 0:
				item, score, rank = rec_from_file.split(':')
				recs.append((int(item), float(score), int(rank)))
				

		return [recs]
		
		

def recommend_users(dataset_ts, dataset_vs, from_file, subm=False):
	
	filename = "from_file.txt"
	ev = evaluator(dataset_vs, 500, filename, subm=subm)
	
	recommender = from_file_recommender(from_file)
	
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
	recommend_users(dataset_ts, dataset_vs, 'datasets/' + ds_name +'/MAP_ucf_cosine_binary_alpha=0.3_mnn=50_q=1.subm')
	

	
	

	
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
	
	
	
	
