from dataset import dataset
import math
import time

class user_distance:
	def __init__(self, dataset, method, construction, alpha=0.5):
		self.dataset = dataset
		self.method = method
		self.construction = construction
		self.alpha = alpha
		
		if method == 'cosine':
			self.distance_method = self.cosine_binary if construction == 'binary' else self.cosine
			self.distance_type = 'similarity'
		

	
	
	def nearestNeighboors(self, user):
		distances = self.dist(user)
		
		# if user == 65537:
			# print user, self.dataset.index2user[user]
			# for user_b in distances:
				# print user_b, self.dataset.index2user[user_b], distances[user_b]
		
		return sorted(distances.items(), key=lambda x: x[1], reverse = self.distance_type == 'similarity')
	
	
	
	
	def dist(self, user):	
		user_item_matrix = self.dataset.user_item_matrix[self.construction]
		item_user_matrix = self.dataset.item_user_matrix[self.construction]
		
		# find all users with at least one song in common:
		users_to_compute = set()
		for item in user_item_matrix[user]:
			for v in item_user_matrix[item]:
				if v != user:
					users_to_compute.add(v)
		
		# for all those users, compute the distance:
		distances = {}
		for v in users_to_compute:
			distances[v] = self.distance_method(user_item_matrix[user], user_item_matrix[v], user_a=user, user_b=v)
		
		return distances
		
		
	
	def cosine(self, a, b, user_a=None, user_b=None):
		dot_a_b = reduce(lambda x, y: x+y, map(lambda x: a[x] * b[x] if x in b else 0, a.iterkeys()))
		if dot_a_b > 0:
			len_a = reduce(lambda x, y: x+y, map(lambda x: x*x, a.itervalues()))
			len_b = reduce(lambda x, y: x+y, map(lambda x: x*x, b.itervalues()))
			dist = float(dot_a_b) / (math.pow(len_a, self.alpha) * math.pow(len_b, (1.0 - self.alpha)))
		else:
			dist = 0
		# if user_a == 37244 and user_b == 98400:
			# print a
			# print b
			# print len_a, len_b, dot_a_b, dist
		return dist

		
		
	def cosine_binary(self, a, b, user_a=None, user_b=None):
		dot_a_b = float(len(set(a) & set(b)))
		if dot_a_b > 0:
			len_a = len(a)
			len_b = len(b)
			dist = dot_a_b / (math.pow(len_a, self.alpha) * (math.pow(len_b, (1.0 - self.alpha))))
		else:
			dist = 0
		# if user_a == 37244 and user_b == 98400:
			# print a
			# print b
			# print alpha, len_a, math.pow(len_a, self.alpha), len_b, math.pow(len_b, self.alpha), dot_a_b, dist
		return dist
		

if __name__ == '__main__':
	dataset = dataset('kaggle_visible_evaluation_triplets_ts.txt')
	user_a = 37244
	user_b = 98400
	a = dataset.user_item_matrix['binary'][user_a]
	b = dataset.user_item_matrix['binary'][user_b]
	print a
	print b
	dist = user_distance(dataset, 'cosine', 'binary')
	print dist.cosine(a, b, user_a=user_a, user_b=user_b)
	
	
	res1 = dist.nearestNeighboors(user_a)
	
	print len(res1)
	print res1[:5]
	
	# users = sorted(dataset.user_item_matrix['count'].iterkeys())
	# n = len(users)
	
	# sti = time.clock()
	# i = 0
	

	# for user in users:
	
		# i += 1
		# if i % 100 == 00:
			# cti = time.clock()
			# t = cti - sti
			# print "%d / %d) tot secs: %f (%f / user)"%(i, n, t,t/(i+1))
		
		# dist.nearestNeighboors(user)
	
	
	# a = {'s': 4.75, 't': 4.5, 'u': 5, 'v': 4.25, 'w': 4}
	# b = {'s': 4, 't': 3, 'u': 5, 'v': 2, 'w': 1}
	# print simi.cosine(a, b)
	