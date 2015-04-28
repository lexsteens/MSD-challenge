from dataset import dataset
import math
import time

class user_distance:
	def __init__(self, dataset, method, construction):
		self.dataset = dataset
		self.method = method
		self.construction = construction
		
		self.distance = {'cosine': self.cosine}		
		
		self.distances = {}
		
	
	
		
	def calculate_similarities(self):		
		user_item_matrix = self.dataset.user_item_matrix
		item_user_matrix = self.dataset.item_user_matrix
		
		users = sorted(user_item_matrix['count'].iterkeys())
		n = len(users)
		
		sti = time.clock()
		i = 0
		
		# iterate on users
		for user in users:
		
			# show timing estimate:
			i += 1
			if i % 100 == 00:
				cti = time.clock()
				t = cti - sti
				print "%d / %d) tot secs: %f (%f / user)"%(i, n, t,t/(i+1))
			
			self.distances[user] = self.dist(user)
	
	
	
	def nearestNeighboors(self, user):
		distances = self.dist(user)
		
		# if user == 65537:
			# print user, self.dataset.index2user[user]
			# for user_b in distances:
				# print user_b, self.dataset.index2user[user_b], distances[user_b]
		
		return sorted(distances.items(), key=lambda x: x[1])
	
	
	
	def dist(self, user):	
		user_item_matrix = self.dataset.user_item_matrix[self.construction]
		item_user_matrix = self.dataset.item_user_matrix[self.construction]
		distance = self.distance[self.method]
		
		# find all users with at least one song in common:
		users_to_compute = set()
		for item in user_item_matrix[user]:
			for v in item_user_matrix[item]:
				if v != user:
					users_to_compute.add(v)
		
		# for all those users, compute the distance:
		distances = {}
		for v in users_to_compute:
			distances[v] = distance(user_item_matrix[user], user_item_matrix[v], user, v)
		
		return distances
		
		
	
	def cosine(self, a, b, user_a, user_b):
		len_a = math.sqrt(reduce(lambda x, y: x+y, map(lambda x: x*x, a.itervalues())))
		len_b = math.sqrt(reduce(lambda x, y: x+y, map(lambda x: x*x, b.itervalues())))
		dot_a_b = reduce(lambda x, y: x+y, map(lambda x: a[x] * b[x] if x in b else 0, a.iterkeys()))
		# if user_a == 65537 and user_b == 3041:
			# print len_a, a
			# print len_b, b
			# print dot_a_b
		return 1. - (1. * dot_a_b / (len_a * len_b))

		
		
if __name__ == '__main__':
	dataset = dataset('kaggle_visible_evaluation_triplets_ts.txt')
	dist = user_distance(dataset, 'cosine', 'count')
	# print dist.nearestNeighboors(65537)
	
	
	users = sorted(dataset.user_item_matrix['count'].iterkeys())
	n = len(users)
	
	sti = time.clock()
	i = 0
	
	# iterate on users
	for user in users:
	
		# show timing estimate:
		i += 1
		if i % 100 == 00:
			cti = time.clock()
			t = cti - sti
			print "%d / %d) tot secs: %f (%f / user)"%(i, n, t,t/(i+1))
		
		dist.nearestNeighboors(user)
	
	
	# a = {'s': 4.75, 't': 4.5, 'u': 5, 'v': 4.25, 'w': 4}
	# b = {'s': 4, 't': 3, 'u': 5, 'v': 2, 'w': 1}
	# print simi.cosine(a, b)
	