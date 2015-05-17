import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties
import sys

ds_name = sys.argv[1]
dir_name = "datasets/%s"%(ds_name)

if ds_name == "sample_1":
	# files = ["MAP_ucf_cosine_binary_alpha=0.3_mnn=50_q=1.txt", "MAP_icf_cosine_binary_alpha=0.8_mnn=50_q=1.txt", "MAP_popularity.txt"]
	# legends = ['# users', 'MAP User Based CF', 'MAP Item Based CF', 'Popularity']
	# plot_styles = ["rs-","yo-","c^-"]
	files = ["MAP_ucf_cosine_binary_alpha=0.3_mnn=50_q=1.txt", "MAP_icf_cosine_binary_alpha=0.8_mnn=50_q=1.txt", "MAP_hybrid_stochastic_set=set1_theta=0.50.txt"]
	legends = ['# users', 'MAP User Based CF', 'MAP Item Based CF', 'MAP Stochastic Aggr']
	plot_styles = ["b.-","yo-","c^-"]
	
	
elif ds_name == "sample_2":
	files = ["MAP_ucf_cosine_binary_alpha=0.3_mnn=50_q=1.txt", "MAP_icf_cosine_binary_alpha=0.85_mnn=50_q=1.txt", "MAP_popularity.txt"]
	plot_styles = ["m^-","rs-","b*-","yo-","c^-"]



hist_max = 50


# Loading history lengths:
# ------------------------
user_history_length = {}
f = open("%s/user_history_lengths.txt"%(dir_name), 'r')
for line in f.readlines():
	user, length = line.strip().split(' ')
	user_history_length[int(user)] = int(length)
f.close()

# Create length history distribution:
users_with_history_length = {}		
for user, history_length in user_history_length.items():	
	if history_length not in users_with_history_length:
		users_with_history_length[history_length] = []
	users_with_history_length[history_length].append(user)

history_lengths = sorted(users_with_history_length.keys())
history_length_dist = []
for history_length in history_lengths:
	history_length_dist.append(len(users_with_history_length[history_length]))


# Start plotting:
leg = []
fig, ax1 = plt.subplots()
val, = ax1.plot(history_lengths[:hist_max], history_length_dist[:hist_max], 'k.:')
leg.append(val)
ax1.set_ylabel('number of users', color='g')
ax1.set_xlabel('history length')
for tl in ax1.get_yticklabels():
	tl.set_color('g')
	

# Loading evaluations:
# --------------------
MAP_dist = {}
for file in files:
	avePs_for_history_length = [[] for i in range(len(history_lengths))]
	with open("%s/%s"%(dir_name, file), 'r') as f:
		for line in f:
			if line.startswith('all') or line.startswith('MAP') or line.startswith('MrecR'):
				continue
			
			if line.find('\t') == -1:
				user, aveP = line.strip().split(' ')
				user, aveP = (int(user), float(aveP))
			else:
				user = int(line[:11])
				aveP = float(line[12:17])
				MrecR = float(line[19:24])
			
			history_length = user_history_length[user]
			idx = history_lengths.index(history_length)
			avePs_for_history_length[idx].append(aveP)
	
	# print avePs_for_history_length[48]
	MAP_dist[file] = []
	for idx, avePs in enumerate(avePs_for_history_length):
		MAP_dist[file].append(np.mean(avePs))
	



	

	
ax2 = ax1.twinx()
for file in files:
	val, = ax2.plot(history_lengths[:hist_max], MAP_dist[file][:hist_max], plot_styles.pop())
	leg.append(val)
ax2.set_ylabel('MAP', color='b')
for tl in ax2.get_yticklabels():
	tl.set_color('b')


	
	
fontP = FontProperties()
fontP.set_size('medium')
print plt.legend(leg, legends, bbox_to_anchor=(0.55, 1), prop = fontP)	

plt.show()
	
sys.exit()










MAP_by_history_length = {}
dist_of_history_length = {}
aveP_at_zero_by_history_length = {}
for history_length, avePs in users_with_history_length.items():
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