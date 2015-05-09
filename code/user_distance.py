from dataset import dataset
import math
import time

class user_distance:
	def __init__(self, dataset, method, construction, alpha=0.5):
		self.dataset = dataset
		self.method = method
		self.construction = construction
		self.alpha = alpha
		
		self.user_length = {}
		u2i = self.dataset.user_item_matrix[construction]		
		for user in u2i:
			self.user_length[user] = sum([count * count for count in u2i[user].values()])
		
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
		item_user_matrix = self.dataset.item_user_matrix[self.dataset.item_user_constructions[0]]
		
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
		
		
	
	def cosine(self, a, b, user_a, user_b):
		dot_a_b = sum([a[item] * b[item] if item in b else 0 for item in a.iterkeys()])
		if dot_a_b > 0:
			dist = float(dot_a_b) / (math.pow(self.user_length[user_a], self.alpha) * math.pow(self.user_length[user_b], (1.0 - self.alpha)))
		else:
			dist = 0
		# if user_a == 37244 and user_b == 98400:
			# print a
			# print b
			# print self.user_length[user_a], self.user_length[user_b], dot_a_b, dist
		return dist

		
		
	def cosine_binary(self, a, b, user_a, user_b):
		dot_a_b = len(set(a) & set(b))
		if dot_a_b > 0:
			dist = float(dot_a_b) / (math.pow(self.user_length[user_a], self.alpha) * (math.pow(self.user_length[user_b], (1.0 - self.alpha))))
		else:
			dist = 0
		# if user_a == 37244 and user_b == 98400:
			# print a
			# print b
			# print alpha, self.user_length[user_a], math.pow(self.user_length[user_a], self.alpha), self.user_length[user_b], math.pow(self.user_length[user_b], self.alpha), dot_a_b, dist
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
	print dist.cosine(a, b, user_a, user_b)
	
	
	res1 = dist.nearestNeighboors(user_a)
	
	print len(res1)
	print res1[:5]
	
	users = sorted(dataset.user_item_matrix['binary'].iterkeys())
	n = len(users)
	
	sti = time.clock()
	i = 0
	
	sumLengths = 0
	minLengths = 99999999
	maxLengths = 0
	for user in users:
	
		i += 1
		if i % 100 == 00:
			cti = time.clock()
			t = cti - sti
			print "%d / %d) tot secs: %f (%f / user)"%(i, n, t,t/(i+1))
		
		nn = dist.nearestNeighboors(user)
		l = len(nn)
		sumLengths += l
		minLengths = min(l, minLengths)
		maxLengths = max(l, maxLengths)
	print sumLengths/len(users)
	print minLengths
	print maxLengths
	
	
	# a = {'s': 4.75, 't': 4.5, 'u': 5, 'v': 4.25, 'w': 4}
	# b = {'s': 4, 't': 3, 'u': 5, 'v': 2, 'w': 1}
	# print dist.cosine(a, b)
	