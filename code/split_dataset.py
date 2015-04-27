

f = open('kaggle_visible_evaluation_triplets.txt', 'r')
user_to_songs = {}
for line in f:
	user, song, count = line.strip().split('\t')
	
	if user in user_to_songs:
		user_to_songs[user].add((song, count))
	else:
		user_to_songs[user] = set([(song, count)])
f.close()


ts = open('kaggle_visible_evaluation_triplets_ts.txt', 'w')
vs = open('kaggle_visible_evaluation_triplets_vs.txt', 'w')
for user in user_to_songs:
	l = len(user_to_songs[user])
	if l >= 0:
		i = 0
		for song in user_to_songs[user]:
			i += 1
			if i <= 3*l/6:
				ts.write('\t'.join([user, song[0], song[1]]) + '\n')
			else:
				vs.write('\t'.join([user, song[0], song[1]]) + '\n')
			
ts.close()
vs.close()