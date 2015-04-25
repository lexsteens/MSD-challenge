from user_item_matrix import user_item_matrix
import math

class user_similarities:
	def __init__(self, user_item_matrix):
		self.user_item_matrix = user_item_matrix
		self.similarities = {}
		self.calculate_similarities()
	
	
		
	def calculate_similarities(self):		
		matrix = self.user_item_matrix.matrix
		user_list = self.user_item_matrix.user_list
		users = sorted(user_list.itervalues())
		n = len(users)
		
		self.similarities['cosine'] = {}
		self.similarities['cosine']['binary'] = [[0.] * n] * n
		self.similarities['cosine']['count'] = [[0.] * n] * n
		print users[:4]
		
		i = 0
		sim = []
		for u in users:
			i += 1
			if i % 100 == 00:
				print i
				
			
			for v in users:
				a = 1
				#self.similarities['cosine']['binary'][u][v] = self.cosine(matrix['binary'][u], matrix['binary'][v])
				#print u, v, self.similarities['cosine']['binary']
				
			
		
	
	def cosine(self, a, b):
		len_a = math.sqrt(reduce(lambda x, y: x+y, map(lambda x: x*x, a.itervalues())))
		len_b = math.sqrt(reduce(lambda x, y: x+y, map(lambda x: x*x, b.itervalues())))
		dot_a_b = reduce(lambda x, y: x+y, map(lambda x: a[x] * b[x] if x in b else 0, a.iterkeys()))
		return 1. * dot_a_b / (len_a * len_b)
	
	def nearestNeighboors(self, user, method, construction):
		a = 1 
		
	
if __name__ == '__main__':
	matrix = user_item_matrix()
	simi = user_similarities(matrix)
	# a = {'s': 4.75, 't': 4.5, 'u': 5, 'v': 4.25, 'w': 4}
	# b = {'s': 4, 't': 3, 'u': 5, 'v': 2, 'w': 1}
	# print simi.cosine(a, b)
	