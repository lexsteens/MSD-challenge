import sys
import datetime
from dataset import dataset

class evaluator:
	def __init__(self, dataset, K, filename, subm=False):
		self.dataset = dataset
		self.dir = self.dataset.dir
		self.filename = filename
		vs = dataset.user_item_matrix['count']
		
		
		self.subm = subm
		if self.subm:
			self.filename_subm = filename.replace('.txt', '.subm')
			self.subm_f = open(self.dir + self.filename_subm, 'w')
		
		# print len(vs)
		# print vs[65537]
		
		vs_ranked = {}
		for user in vs:
			vs_ranked[user] = map(lambda x: x[0], sorted(vs[user].items(), key=lambda x: x[1], reverse=True))
			
		# print len(vs_ranked)
		# print vs_ranked[65537]
		
		self.vs = vs
		self.vs_ranked = vs_ranked
		self.K = K
		
		self.results = {}
		
		print "evaluator ready."
			
		
	
	
	def save_details(self):
		with open(self.dir + self.filename, 'w') as f:
			f.write(' '.join(['MAP', str(self.get_MAP())]) + "\n")
			f.write(' '.join(['MrecR', str(self.get_MrecR())]) + "\n")
			for user, result in self.results.items():
				aveP = "%.4f" % result['aveP']
				recRank = "%.4f" % result['recRank']
				corrects = ' '.join([str(item) + '@' + str(rank) for item, rank in result['corrects']])
				f.write(' '.join([str(user).ljust(10), aveP, recRank]) + '\t' + corrects + "\n")
			
	
	
		
	def get_MAP(self):
		return reduce(lambda x, y: x+y, [result['aveP'] for user, result in self.results.items()]) / len(self.results)
		
		
		
	def get_MrecR(self):
		return reduce(lambda x, y: x+y, [result['recRank'] for user, result in self.results.items()]) / len(self.results)
		
		
		
		
		
	def add_ranking(self, user, full_ranking):
		ranking = [item for item, score, rank in full_ranking]
		ranking_vs = self.vs_ranked[user]
		
		self.results[user] = self.aveP(ranking, ranking_vs, user)
		
		if self.subm:
			self.subm_f.write(str(user).ljust(10) + '\t' + ' '.join([str(item) + ':' + str(round(score, 4)) + ':' + str(rank + 1) for item, score, rank in full_ranking]) + '\n')

		
		
		
	def aveP(self, ranking, ranking_vs, user):
		# print user
		rank = 0
		correct_items = 0.
		sumPrec = 0.
		first = 0
		corrects = []
		
		for item in ranking[:self.K]:
			rank += 1
			
			if item in ranking_vs:
				correct_items += 1
				corrects.append((item, rank))
				
				prec = correct_items / rank
				# print "Precision @", rank, ":", prec, '(', self.dataset.index2item[item], ')'
				sumPrec += prec
				
				if first == 0:
					first = rank
		
		denom = min(correct_items, self.K)
		# if denom == 0:
			# print "Denom = 0 for user:", user, self.dataset.index2user[user], denom
		aveP  = sumPrec / denom if denom > 0 else 0
		recRank = 1. / first if first > 0 else 0
		
		# print "Average Precision @", self.K, ":", aveP
		# print "Reciprocal Rank : ", recRank
		
		return {'aveP': aveP, 'recRank': recRank, 'corrects': corrects}
		
		
	

		
		



if __name__ == '__main__':
	dataset = dataset('kaggle_visible_evaluation_triplets_vs.txt')
	evaluator = evaluator(dataset, 500)
	
	


	
