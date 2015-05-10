from dataset import dataset
import math
import time

class item_distance:
	def __init__(self, dataset, method, construction, alpha=0.5):
		self.dataset = dataset
		self.method = method
		self.construction = construction
		self.alpha = alpha
		
		self.item_length = {}
		i2u = self.dataset.item_user_matrix[construction]		
		for item in i2u:
			self.item_length[item] = sum([count * count for count in i2u[item].values()])
		
		if method == 'cosine':
			self.distance_method = self.cosine_binary if construction == 'binary' else self.cosine
			self.distance_type = 'similarity'
		

	
	
	def nearestNeighboors(self, item):
		distances = self.dist(item)
		
		return sorted(distances.items(), key=lambda x: x[1], reverse = self.distance_type == 'similarity')
	
	
	
	
	def dist(self, item):
		item_user_matrix = self.dataset.item_user_matrix[self.construction]
		user_item_matrix = self.dataset.user_item_matrix[self.dataset.item_user_constructions[0]]
		
		# find all items with at least one user in common:
		items_to_compute = set()
		for user in item_user_matrix[item]:
			for j in user_item_matrix[user]:
				if j != item:
					items_to_compute.add(j)
		
		# for all those users, compute the distance:
		distances = {}
		for j in items_to_compute:
			distances[j] = self.distance_method(item, j)
		
		return distances
		
		
	
	def cosine(self, item_a, item_b):
		a = self.dataset.item_user_matrix[self.construction][item_a]
		b = self.dataset.item_user_matrix[self.construction][item_b]
		dot_a_b = sum([a[user] * b[user] if user in b else 0 for user in a.iterkeys()])
		
		if dot_a_b > 0:
			dist = float(dot_a_b) / (math.pow(self.item_length[item_a], self.alpha) * math.pow(self.item_length[item_b], (1.0 - self.alpha)))
		else:
			dist = 0
			
		# print dot_a_b, self.item_length[item_a], math.pow(self.item_length[item_a], self.alpha), self.item_length[item_b], math.pow(self.item_length[item_b], (1.0 - self.alpha)), dist
		
		return dist

		
		
	def cosine_binary(self, item_a, item_b):
		a = self.dataset.item_user_matrix[self.construction][item_a]
		b = self.dataset.item_user_matrix[self.construction][item_b]
		dot_a_b = len(set(a) & set(b))
		
		if dot_a_b > 0:
			dist = float(dot_a_b) / (math.pow(self.item_length[item_a], self.alpha) * (math.pow(self.item_length[item_b], (1.0 - self.alpha))))
		else:
			dist = 0
			
		# print dot_a_b, self.item_length[item_a], math.pow(self.item_length[item_a], self.alpha), self.item_length[item_b], math.pow(self.item_length[item_b], (1.0 - self.alpha)), dist
		
		return dist
		

if __name__ == '__main__':
	dataset = dataset('kaggle_visible_evaluation_triplets_ts.txt')	
	dist = item_distance(dataset, 'cosine', 'binary')
	# item_a = 384595
	# item_b = 254590
	# a = dataset.item_user_matrix['binary'][item_a]
	# b = dataset.item_user_matrix['binary'][item_b]
	# print a
	# print b
	# print dist.cosine(item_a, item_b)
	# print dist.cosine_binary(item_a, item_b)
	
	
	# res1 = dist.nearestNeighboors(item_a)
	
	# print len(res1)
	# print res1
	
	items = sorted(dataset.item_user_matrix['binary'].iterkeys())
	n = len(items)
	
	sti = time.clock()
	i = 0
	
	sumLengths = 0
	minLengths = 99999999
	maxLengths = 0
	for item in items:
	
		i += 1
		if i % 100 == 00:
			cti = time.clock()
			t = cti - sti
			print "%d / %d) tot secs: %f (%f / item)"%(i, n, t,t/(i+1))
		
		nn = dist.nearestNeighboors(item)
		l = len(nn)
		sumLengths += l
		minLengths = min(l, minLengths)
		maxLengths = max(l, maxLengths)
	print sumLengths/len(items)
	print minLengths
	print maxLengths
	
	
	# a = {'s': 4.75, 't': 4.5, 'u': 5, 'v': 4.25, 'w': 4}
	# b = {'s': 4, 't': 3, 'u': 5, 'v': 2, 'w': 1}
	# print dist.cosine(a, b)
	