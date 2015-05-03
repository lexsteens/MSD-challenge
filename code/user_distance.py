from dataset import dataset
import math
import time

class user_distance:
	def __init__(self, dataset, method, construction):
		self.dataset = dataset
		self.method = method
		self.construction = construction
		
		self.distance = {
			'cosine': {'func': self.cosine, 'type': 'similarity'},
			'cosine2': {'func': self.cosine2, 'type': 'similarity'}
		}		
		
		self.distances = {}
	
	
	
	def nearestNeighboors(self, user):
		distances = self.dist(user)
		
		# if user == 65537:
			# print user, self.dataset.index2user[user]
			# for user_b in distances:
				# print user_b, self.dataset.index2user[user_b], distances[user_b]
		
		return sorted(distances.items(), key=lambda x: x[1], reverse = self.distance[self.method]['type'] == 'similarity')
	
	
	
	def dist(self, user):	
		user_item_matrix = self.dataset.user_item_matrix[self.construction]
		item_user_matrix = self.dataset.item_user_matrix[self.construction]
		distance_method = self.distance[self.method]['func']
		
		# find all users with at least one song in common:
		users_to_compute = set()
		for item in user_item_matrix[user]:
			for v in item_user_matrix[item]:
				if v != user:
					users_to_compute.add(v)
		
		# for all those users, compute the distance:
		distances = {}
		for v in users_to_compute:
			distances[v] = distance_method(user_item_matrix[user], user_item_matrix[v], user_a=user, user_b=v)
		
		return distances
		
		
	
	def cosine(self, a, b, user_a=None, user_b=None):
		len_a = reduce(lambda x, y: x+y, map(lambda x: x*x, a.itervalues()))
		len_b = reduce(lambda x, y: x+y, map(lambda x: x*x, b.itervalues()))
		dot_a_b = reduce(lambda x, y: x+y, map(lambda x: a[x] * b[x] if x in b else 0, a.iterkeys()))
		dist = float(dot_a_b) / (math.sqrt(len_a) * math.sqrt(len_b))
		if user_a == 37244 and user_b == 98400:
			print a
			print b
			print len_a, len_b, dot_a_b, dist
		return dist

		
		
	def cosine2(self, a, b, alpha=0.5, user_a=None, user_b=None):
		w = float(len(set(a) & set(b)))
		if w > 0:
			l1 = len(a)
			l2 = len(b)
			dist = w / (math.pow(l1, alpha) * (math.pow(l2, (1.0 - alpha))))	
		if user_a == 37244 and user_b == 98400:
			print a
			print b
			print alpha, l1, math.pow(l1, alpha), l2, math.pow(l2, alpha), w, dist
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
	print dist.cosine2(a, b, alpha=0.5, user_a=user_a, user_b=user_b)
	
	dist2 = user_distance(dataset, 'cosine2', 'binary')
	
	res1 = dist.nearestNeighboors(user_a)
	res2 = dist2.nearestNeighboors(user_a)
	
	print len(res1), len(res2)
	print res1[:5]
	print res2[:5]
	
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
	