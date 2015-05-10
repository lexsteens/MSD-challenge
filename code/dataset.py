import math

class dataset:
	def __init__(self, filename, user_item_constructions=['binary'], item_user_constructions=['binary']):
		self.filename = filename
		self.dir = "datasets/" + filename[:-7] + "/"
		print self.dir
	
		self.user_item_constructions=user_item_constructions
		self.item_user_constructions=item_user_constructions
	
		self.user2index = {}
		self.index2user = {}
		self.item2index = {}
		self.index2item = {}
		
		self.user_item_matrix = {}
		for construction in user_item_constructions:
			self.user_item_matrix[construction] = {}
		
		self.item_user_matrix = {}
		for construction in item_user_constructions:
			self.item_user_matrix[construction] = {}
		
		self.load_user_indexes()
		self.load_item_indexes()
		self.load_matrixes()
		
		if 'norm' in self.user_item_constructions:
			self.normalise_users()
		if 'tfidf' in self.user_item_constructions:
			self.tfidf_users()
			
		# if 'norm' in self.item_user_constructions:
			# self.normalise_items()
		# if 'tfidf' in self.item_user_constructions:
			# self.tfidf_items()	
			
			
	
	def load_user_indexes(self):
		print 'loading user indexes...'
		f = open(self.dir + 'kaggle_users.txt', 'r')
		i = 0
		for line in f:
			i += 1
			user = line.strip()
			self.user2index[user] = i
			self.index2user[i] = user
		f.close()
		print "done."
		
	
	
	def load_item_indexes(self):
		print 'loading item indexes...'
		f = open(self.dir + 'kaggle_songs.txt', 'r')
		for line in f:
			item, i = line.strip().split(" ")
			i = int(i)
			self.item2index[item] = i
			self.index2item[i] = item
		f.close()
		print "done."
		
	
	
	def load_matrixes(self):
		print 'loading evaluation triplets...'
		f = open(self.dir + self.filename, 'r')

		for line in f:
			user, item, count = line.strip().split('\t')
			self.add_line(user, item, int(count))

		f.close()
		print "done."
		
		
	
	def add_line(self, user, item, count):
			user_index = self.user2index[user]
			item_index = self.item2index[item]
			
			# updating user_item_matrix:
			# --------------------------
			for construction in self.user_item_constructions:
				if user_index not in self.user_item_matrix[construction]:
					self.user_item_matrix[construction][user_index] = {}
			
			if 'count' in self.user_item_constructions:
				self.user_item_matrix['count'][user_index][item_index] = count
			if 'binary' in self.user_item_constructions:
				self.user_item_matrix['binary'][user_index][item_index] = 1
			if 'norm' in self.user_item_constructions:
				self.user_item_matrix['norm'][user_index][item_index] = count
			if 'tfidf' in self.user_item_constructions:
				self.user_item_matrix['tfidf'][user_index][item_index] = count
			
			
			# updating item_user_matrix:
			# --------------------------
			for construction in self.item_user_constructions:
				if item_index not in self.item_user_matrix[construction]:
					self.item_user_matrix[construction][item_index] = {}
			
			if 'count' in self.item_user_constructions:
				self.item_user_matrix['count'][item_index][user_index] = count
			if 'binary' in self.item_user_constructions:
				self.item_user_matrix['binary'][item_index][user_index] = 1
			# if 'norm' in self.item_user_constructions:
				# self.item_user_matrix['norm'][item_index][user_index] = count
			# if 'tfidf' in self.item_user_constructions:
				# self.item_user_matrix['tfidf'][item_index][user_index] = count
	
	
	def normalise_users(self):
		u2i = self.user_item_matrix['norm']
		for user in u2i:
			# if user == 32500:
				# print u2i[user]
			norm = math.sqrt(sum([count * count for count in u2i[user].values()]))
			for item in u2i[user]:
				u2i[user][item] = float(u2i[user][item]) / norm
			# if user == 32500:
				# print u2i[user]
	
	
	def tfidf_users(self):
		# term frequency(i) = number of time user listen to song(i) (=count)
		# document frequency(i) = number of user listening to song(i)
	
		# number of documents (users):
		N = len(self.user_item_matrix['tfidf'])
	
		idf = {}
		# use a item_user_matrix to calculate document (user) frequencies:
		i2u = self.item_user_matrix[self.item_user_constructions[0]]
		for item in i2u:
			df = len(set(i2u[item]))
			idf[item] = math.log(N/df, 10)
		
		# calculate normalized tfidf weights:
		u2i = self.user_item_matrix['tfidf']
		for user in u2i:
			# if user == 32500:
				# print u2i[user]
			# the norm is the square root of term frequencies:
			norm = math.sqrt(sum([count * count for count in u2i[user].values()]))
			for item in u2i[user]:
				u2i[user][item] = float(u2i[user][item]) * idf[item] / norm
			# if user == 32500:
				# print u2i[user]
	
	
	
if __name__ == '__main__':

	matrix = dataset('kaggle_visible_evaluation_triplets_ts.txt', user_item_constructions=['norm', 'tfidf']);
	print matrix.user_item_matrix.keys()
	print matrix.item_user_matrix.keys()
	input('...')
	
	# print matrix.user2index['b40ff7e719c613dae8505b5112e3f99fe7ced78c']
	# print matrix.index2user[5]
	# print
	# print matrix.item2index['SOZZYVC12A8C13932C']
	# print matrix.index2item[279780]
	# print
	# print matrix.user_item_matrix['count'][5]
	# print matrix.index2user[5]
	# print map(lambda x: (matrix.index2item[x[0]], x[1]), matrix.user_item_matrix['count'][5].iteritems())
	# print
	# print matrix.item_user_matrix['count'][183117]
	# print matrix.index2item[183117]
	# print map(lambda x: (matrix.index2user[x[0]], x[1]), matrix.item_user_matrix['count'][183117].iteritems())
		

	# matrix = user_item_matrix()
	# matrix_count = matrix.get_matrix('count')
	# matrix_binary = matrix.get_matrix('binary')
	
	# print matrix.user_list['04cd8d64e32be6c37a609d4cd548d6947c613829']
	# print matrix_count[0]
	# print matrix_binary[0]
	