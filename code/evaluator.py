import sys
import datetime
from dataset import dataset

class evaluator:
	def __init__(self, dataset, K):
		self.dataset = dataset
		vs = dataset.user_item_matrix['count']
		
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
		self.sumAveP = 0.
		self.numUsers = 0
		
		self.average_precision = {}
		
		print "evaluator ready."
			
		
	
	
	def save_details(self, filename):
		with open(filename, 'w') as f:
			for user, value in self.average_precision.items():
				f.write(' '.join([str(user), str(value)]) + "\n")
			
	
	
		
	def get_MAP(self):
		return reduce(lambda x, y: x+y, [value for item, value in self.average_precision.items()]) / len(self.average_precision)
		
		
		
		
		
	def add_ranking(self, user, ranking):
		ranking = [item for item, score, rank in ranking]
		ranking_vs = self.vs_ranked[user]
		
		self.average_precision[user] = self.aveP(ranking, ranking_vs, user)
		
		# if user < 25:
			# print ranking[:25]
			# print ranking_vs[:25]
			# print self.optimized_aveP(ranking, ranking_vs, user)
			# print self.sumAveP, self.sumAveP / self.numUsers, self.get_MAP()
		
		
		
	def aveP(self, ranking, ranking_vs, user):
		# print user
		level = 0
		correct_items = 0.
		sumPrec = 0.
		
		for item in ranking[:self.K]:
			level += 1
			
			if item in ranking_vs:
				correct_items += 1
				prec = correct_items / level
				# print "Precision @", level, ":", prec, '(', self.dataset.index2item[item], ')'
				sumPrec += prec
		
		denom = min(correct_items, self.K)
		# if denom == 0:
			# print "Denom = 0 for user:", user, self.dataset.index2user[user], denom
		res  = sumPrec / denom if denom > 0 else 0
		
		# print "Average Precision @", self.K, ":", res
		
		return res
		
		
	

		
		



if __name__ == '__main__':
	dataset = dataset('kaggle_visible_evaluation_triplets_vs.txt')
	evaluator = evaluator(dataset, 500)
	
	


	
