import sys
import datetime
from dataset import dataset

class evaluator:
	def __init__(self, dataset, K):
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
		
		print "evaluator ready."
		
	def add_ranking(self, user, ranking):
		ranking_vs = self.vs_ranked[user]
		# print user
		# print ranking[:100]
		# print ranking_vs
		# print user, self.aveP(ranking, ranking_vs, user)
		self.sumAveP += self.aveP(ranking, ranking_vs, user)
		self.numUsers += 1
	
	def aveP(self, ranking, ranking_vs, user):
	
		# if user == 65537:
			# print user
			# for d in ranking[:20]:
				# print d, d in ranking_vs
				
		sumPrec = reduce(lambda x,y: x+y, map(lambda l: self.precision(l + 1, ranking, ranking_vs, user) if ranking[l] in ranking_vs else 0, range(min(len(ranking), self.K))), 0.)
		denom = min(len(filter(lambda x: x in ranking, ranking_vs)), self.K)
		res = sumPrec / denom if denom > 0 else 0

		# if user == 65537:
			# print range(min(len(ranking), self.K))
			# print "Average Precision @", self.K, ":", sumPrec, "/", denom, "=", res
		
		return res
		
		
		
	def optimized_aveP(self, ranking, ranking_vs):
		for i in range(self.K):
			a = 1
		
		
	
	def precision(self, l, ranking, ranking_vs, user):
		res = 1. * reduce(lambda x,y: x+y, map(lambda d: 1 if d in ranking_vs else 0, ranking[:l])) / l
		
		if user == 65537:
			print "Precision @", l, ":", res
		return res
			
		
		
		
	def get_MAP(self):
		return self.sumAveP / self.numUsers

		
		



if __name__ == '__main__':
	dataset = dataset('kaggle_visible_evaluation_triplets_vs.txt')
	evaluator = evaluator(dataset, 500)
	
	


	
