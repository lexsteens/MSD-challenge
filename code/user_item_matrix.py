

class dataset:
	def __init__(self, filename):		
		self.user2index = {}
		self.index2user = {}
		self.item2index = {}
		self.index2item = {}
		
		self.user_item_matrix = {}
		self.user_item_matrix['count'] = {}
		self.user_item_matrix['binary'] = {}
		
		self.item_user_matrix = {}
		self.item_user_matrix['count'] = {}
		self.item_user_matrix['binary'] = {}
		
		self.load_user_indexes()
		self.load_song_indexes()
		self.load_matrixes(filename)
	
	
	def load_user_indexes(self):
		print 'loading user indexes...'
		f = open('kaggle_users.txt', 'r')
		i = 0
		for line in f:
			i += 1
			user = line.strip()
			self.user2index[user] = i
			self.index2user[i] = user
		f.close()
		print "done."
	
	
	def load_song_indexes(self):
		print 'loading song indexes...'
		f = open('kaggle_songs.txt', 'r')
		for line in f:
			song, i = line.strip().split(" ")
			i = int(i)
			self.item2index[song] = i
			self.index2item[i] = song
		f.close()
		print "done."
	
	
	def load_matrixes(self, filename):
		print 'loading evaluation triplets...'
		f = open(filename, 'r')

		for line in f:
			user, song, count = line.strip().split('\t')
			self.add_line(user, song, int(count))

		f.close()
		print "done."
		
	
	def add_line(self, user, song, count):
			user_index = self.user2index[user]
			song_index = self.item2index[song]
			
			# updating user_item_matrix:
			# --------------------------
			if user_index not in self.user_item_matrix['count']:
				self.user_item_matrix['count'][user_index] = {}
				self.user_item_matrix['binary'][user_index] = {}
				
			self.user_item_matrix['count'][user_index][song_index] = count
			self.user_item_matrix['binary'][user_index][song_index] = 1
			
			
			# updating item_user_matrix:
			# --------------------------
			if song_index not in self.item_user_matrix['count']:
				self.item_user_matrix['count'][song_index] = {}
				self.item_user_matrix['binary'][song_index] = {}
			
			self.item_user_matrix['count'][song_index][user_index] = count
			self.item_user_matrix['binary'][song_index][user_index] = 1
	
	
if __name__ == '__main__':

	matrix = dataset('kaggle_visible_evaluation_triplets_ts.txt');
	
	print matrix.user2index['b40ff7e719c613dae8505b5112e3f99fe7ced78c']
	print matrix.index2user[5]
	print
	print matrix.item2index['SOZZYVC12A8C13932C']
	print matrix.index2item[279780]
	print
	print matrix.user_item_matrix['count'][5]
	print matrix.index2user[5]
	print map(lambda x: (matrix.index2item[x[0]], x[1]), matrix.user_item_matrix['count'][5].iteritems())
	print
	print matrix.item_user_matrix['count'][136139]
	print matrix.index2item[136139]
	print map(lambda x: (matrix.index2user[x[0]], x[1]), matrix.item_user_matrix['count'][136139].iteritems())
		

	# matrix = user_item_matrix()
	# matrix_count = matrix.get_matrix('count')
	# matrix_binary = matrix.get_matrix('binary')
	
	# print matrix.user_list['04cd8d64e32be6c37a609d4cd548d6947c613829']
	# print matrix_count[0]
	# print matrix_binary[0]
	