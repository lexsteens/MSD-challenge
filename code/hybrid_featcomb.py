from evaluator import evaluator
from dataset import dataset
from from_file import from_file_recommender
import time
import json
import sys
import random



global_debug_info = {}

class hybrid_featcomb_recommender:
	def __init__(self, recommenders, thetas=[0.5]):
		self.recommenders = recommenders
		self.thetas = thetas
	
	
	
	def recommend_user(self, user):
		
		rec1 = self.recommenders[0].recommend_user(user)[0]
		rec2 = self.recommenders[1].recommend_user(user)[0]
		
		recs = {}
		for theta in self.thetas:
			scores = {}
			for rec in rec1:
				item, score, rank = rec
				if rec[0] not in scores:
					scores[item] = 0.
				scores[item] += score * theta
			
			for rec in rec2:
				item, score, rank = rec
				if rec[0] not in scores:
					scores[item] = 0.
				scores[item] += score * (1 - theta)

			
			rec = [(t[0], t[1], idx + 1) for idx, t in enumerate(sorted(scores.items(), key=lambda x: x[1], reverse=True))]			
			recs[theta] = rec

		return recs
		
		

		
def recommend_users(ds_name, dataset_ts, dataset_vs, set, thetas=[0.5], subm=False):
	
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
	

	recommender = hybrid_featcomb_recommender([recommender1, recommender2], thetas=thetas)
	
	evaluators = {}
	for theta in thetas:
		filename='MAP_hybrid_featcomb_set=' + set + '_theta=' + "%.2f"%(theta) + '.txt'
		print filename
		evaluators[theta] = evaluator(dataset_vs, 500, filename, subm=subm)
	
	
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
			print ' '.join(["\t%.2f:\t%.4f\n"%(theta, ev.get_MAP()) for theta, ev in sorted(evaluators.items(), key=lambda x: x[1])])
			print
	
		recs = recommender.recommend_user(user)
		
		for theta in recs:
			evaluators[theta].add_ranking(user, recs[theta])
		

	for ev in evaluators.values():
		ev.save_details()
			
			
			
			
			
if __name__ == '__main__':

	ds_name = sys.argv[1]
	set = sys.argv[2]

	dataset_ts = dataset(ds_name + '_ts.txt', user_item_constructions=['binary'], item_user_constructions=['binary'])	
	dataset_vs = dataset(ds_name + '_vs.txt', user_item_constructions=['count'], item_user_constructions=[])
	recommend_users(ds_name, dataset_ts, dataset_vs, set, thetas=[float(x)/100 for x in range(0, 105, 5)])
	# recommend_users(ds_name, dataset_ts, dataset_vs, set, thetas=[0.5])

	
	


	
	
	
	
