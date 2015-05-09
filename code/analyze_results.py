from dataset import dataset
import numpy as np
import matplotlib.pyplot as plt

a = [1, 2]
print np.mean(a)

dataset_ts = dataset('kaggle_visible_evaluation_triplets_ts.txt', user_item_constructions=['count'])

MAP = {}
with open('datasets/kaggle_visible_evaluation_triplets/MAP_cosine_binary_alpha=0.8_q=1.txt', 'r') as f:
	for line in f:
		user_idx, value = line.strip().split(' ')
		if user_idx != 'all':
			MAP[int(user_idx)] = float(value)


length_distribution = {}		
for user_idx, value in MAP.items():
	history_length = len(dataset_ts.user_item_matrix['count'][user_idx])
	user = dataset_ts.index2user[user_idx]
	
	# if history_length == 10:
		# print user_idx
	
	if history_length not in length_distribution:
		length_distribution[history_length] = []
	length_distribution[history_length].append(value)

MAP_by_history_length = {}
dist_of_history_length = {}
aveP_at_zero_by_history_length = {}
for history_length, avePs in length_distribution.items():
	MAP_by_history_length[history_length] = np.mean(avePs)
	dist_of_history_length[history_length] = len(avePs)
	aveP_at_zero_by_history_length[history_length] = len([x for x in avePs if x == 0])

	

axis1 = [hist_length for hist_length, value in sorted(MAP_by_history_length.items(), key=lambda x: x[0])]
MAP_by_history_length = [value for hist_length, value in sorted(MAP_by_history_length.items(), key=lambda x: x[0])]
aveP_at_zero_by_history_length = [value for hist_length, value in sorted(aveP_at_zero_by_history_length.items(), key=lambda x: x[0])]
dist_of_history_length = [value for hist_length, value in sorted(dist_of_history_length.items(), key=lambda x: x[0])]

for idx, i in enumerate(axis1):
	print str(axis1[idx]) + "\t" + str(dist_of_history_length[idx]) + "\t" + str(aveP_at_zero_by_history_length[idx]) + "\t" + str(round(float(aveP_at_zero_by_history_length[idx]) / dist_of_history_length[idx] * 100, 2)) + "%\t" + str(round(MAP_by_history_length[idx], 5))

# plt.plot(axis1, dist_of_history_length, 'gs-')
# plt.plot(axis1, aveP_at_zero_by_history_length, 'ro-')
# plt.show()



fig, ax1 = plt.subplots()
ax1.plot(axis1, dist_of_history_length, 'gs-')
ax1.plot(axis1, aveP_at_zero_by_history_length, 'go-')
ax1.set_ylabel('number of users', color='g')
ax1.set_xlabel('history length')
for tl in ax1.get_yticklabels():
	tl.set_color('g')
	
ax2 = ax1.twinx()
ax2.plot(axis1, MAP_by_history_length, 'b^-')
ax2.set_ylabel('MAP', color='b')
for tl in ax2.get_yticklabels():
	tl.set_color('b')

plt.show()