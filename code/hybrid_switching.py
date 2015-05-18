from evaluator import evaluator
from dataset import dataset
from from_file import from_file_recommender
import time
import json
import sys
import random



global_debug_info = {}

class hybrid_featcomb_recommender:
	def __init__(self, recommenders, hist_lengths, criterias=[10]):
		self.recommenders = recommenders
		self.hist_lengths = hist_lengths
		self.criterias = criterias
	
	
	
	def recommend_user(self, user):
		
		rec1 = self.recommenders[0].recommend_user(user)[0]
		rec2 = self.recommenders[1].recommend_user(user)[0]
		
		recs = {}
		for criteria in self.criterias:
			# print self.hist_lengths[user], criteria, "rec1" if self.hist_lengths[user] > criteria else "rec2"
			rec = rec1 if self.hist_lengths[user] > criteria else rec2	
			recs[criteria] = rec

		return recs
		
		

		
def recommend_users(ds_name, dataset_ts, dataset_vs, set, criterias=[10], subm=False):
	
	sets_file = open('datasets/' + ds_name + '/hybrid_sets.txt', 'r')
	
	found = False
	for line in sets_file.readlines():
		set_name, rec_names = line.strip().split('\t')
		if set_name == set:
			found = True
			rec_names = rec_names.split(' ')
			recommender1 = from_file_recommender('datasets/' + ds_name + '/' + rec_names[0])
			recommender2 = from_file_recommender('datasets/' + ds_name + '/' + rec_names[1])
	sets_file.close()
	
	if found == False:
		raise('No hybrid set ' + set + ' in ' + ds_name)
	
	hist_lengths = {}
	u2i = dataset_ts.user_item_matrix[dataset_ts.user_item_constructions[0]]
	for user in u2i:
		hist_lengths[user] = len(u2i[user])

	recommender = hybrid_featcomb_recommender([recommender1, recommender2], hist_lengths, criterias=criterias)
	
	evaluators = {}
	for criteria in criterias:
		filename='MAP_hybrid_switching_set=' + set + '_criteria=' + "%.2f"%(criteria) + '.txt'
		print filename
		evaluators[criteria] = evaluator(dataset_vs, 500, filename, subm=subm)
	
	
	users = sorted(dataset_ts.user_item_matrix[dataset_ts.user_item_constructions[0]].iterkeys())
	n = len(users)
	
	sti = time.clock()
	i = 0	
	for user in users:		
		i += 1
		if i % 500 == 0 and i > 0:
			cti = time.clock()
			t = cti - sti
			print "%d / %d) tot secs: %f (%f / user)"%(i, n, t,t/(i+1))
			print ' '.join(["\t%.2f:\t%.4f\n"%(criteria, ev.get_MAP()) for criteria, ev in sorted(evaluators.items(), key=lambda x: x[1])])
			print
	
		recs = recommender.recommend_user(user)
		
		for criteria in recs:
			evaluators[criteria].add_ranking(user, recs[criteria])
		

	for ev in evaluators.values():
		ev.save_details()
			
			
			
			
			
if __name__ == '__main__':

	ds_name = sys.argv[1]
	set = sys.argv[2]

	dataset_ts = dataset(ds_name + '_ts.txt', user_item_constructions=['binary'], item_user_constructions=['binary'])	
	dataset_vs = dataset(ds_name + '_vs.txt', user_item_constructions=['count'], item_user_constructions=[])
	# recommend_users(ds_name, dataset_ts, dataset_vs, set, criterias=[float(x)/100 for x in range(0, 105, 5)])
	recommend_users(ds_name, dataset_ts, dataset_vs, set, criterias=[10])

	
	


	
	
	
	
