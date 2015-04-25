from dataset import dataset
import math
import time

class similarities:
	def __init__(self, dataset):
		self.dataset = dataset
		self.similarities = {}
		
		self.calculate_similarities()
	
	
		
	def calculate_similarities(self):		
		user_item_matrix = self.dataset.user_item_matrix
		item_user_matrix = self.dataset.item_user_matrix
		users = sorted(user_item_matrix['count'].iterkeys())
		n = len(users)
		
		self.similarities['cosine'] = {}
		self.similarities['cosine']['binary'] = {}
		self.similarities['cosine']['count'] = {}
		
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
			
			# find all users with at least one song in common:
			users_to_compute = set()
			for item in user_item_matrix['count'][user]:
				for v in item_user_matrix['count'][item]:
					users_to_compute.add(v)
			
			# for all those users, compute the distance:
			self.similarities['cosine']['count'][user] = {}
			for v in users_to_compute:
				self.similarities['cosine']['count'][user][v] = self.cosine(user_item_matrix['count'][user], user_item_matrix['count'][v])
			
		
	
	def cosine(self, a, b):
		len_a = math.sqrt(reduce(lambda x, y: x+y, map(lambda x: x*x, a.itervalues())))
		len_b = math.sqrt(reduce(lambda x, y: x+y, map(lambda x: x*x, b.itervalues())))
		dot_a_b = reduce(lambda x, y: x+y, map(lambda x: a[x] * b[x] if x in b else 0, a.iterkeys()))
		return 1. * dot_a_b / (len_a * len_b)
	
	def nearestNeighboors(self, user, method, construction):
		a = 1 
		
	
if __name__ == '__main__':
	dataset = dataset('kaggle_visible_evaluation_triplets_ts.txt')
	simi = similarities(dataset)
	
	keys = dataset.user_item_matrix['count'].keys()
	a_user_index = keys[0]
	a_user = dataset.index2user[a_user_index]
	print a_user_index, a_user
	for user_index in simi.similarities['cosine']['count'][a_user_index]:
		user = dataset.index2user[user_index]
		sim = simi.similarities['cosine']['count'][a_user_index][user_index]
		print user_index, user, sim
	
	
	# a = {'s': 4.75, 't': 4.5, 'u': 5, 'v': 4.25, 'w': 4}
	# b = {'s': 4, 't': 3, 'u': 5, 'v': 2, 'w': 1}
	# print simi.cosine(a, b)
	