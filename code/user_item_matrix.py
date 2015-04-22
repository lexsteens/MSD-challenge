

class user_item_matrix:
	def __init__(self):
		self.user_count = 0
		self.item_num = 0
		self.user_list = {}
		self.item_list = {}
		self.matrix = {}
		self.matrix['count'] = {}
		self.matrix['binary'] = {}
		
		self.load_user_matrix()
	
	def load_user_matrix(self):
		# loading user matrix
		print 'loading evaluation triplets...'
		f = open('kaggle_visible_evaluation_triplets_ts.txt', 'r')

		for line in f:
			user, song, count = line.strip().split('\t')
			self.add_line(user, song, count)

		f.close()
		print "done."
		
	
	def add_line(self, user, item, count):
				
			if user not in self.user_list:
				self.user_list[user] = self.user_count
				self.user_count += 1
			
			if item not in self.item_list:
				self.item_list[item] = self.item_num
				self.item_num += 1
				
			if self.user_list[user] not in self.matrix['count']:
				self.matrix['count'][self.user_list[user]] = {}
				self.matrix['binary'][self.user_list[user]] = {}
				
			self.matrix['count'][self.user_list[user]][self.item_list[item]] = int(count)
			self.matrix['binary'][self.user_list[user]][self.item_list[item]] = 1
		
	def get_matrix(self, contruction):
		return self.matrix[contruction]
		
	
if __name__ == '__main__':
	matrix = user_item_matrix()
	matrix_count = matrix.get_matrix('count')
	matrix_binary = matrix.get_matrix('binary')
	
	print matrix.user_list['04cd8d64e32be6c37a609d4cd548d6947c613829']
	print matrix_count[0]
	print matrix_binary[0]
	