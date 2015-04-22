from evaluator import evaluator
import sys

f = open('kaggle_visible_evaluation_triplets_ts.txt', 'r')
song_to_count = {}
user_to_songs = {}
for line in f:
	user, song, _ = line.strip().split('\t')
	if song in song_to_count:
		song_to_count[song] += 1
	else:
		song_to_count[song] = 1
		
	if user in user_to_songs:
		user_to_songs[user].add(song)
	else:
		user_to_songs[user] = set([song])
f.close()
print "reading evaluation triplets done."


songs_ordered = sorted(song_to_count.keys(), key=lambda s: song_to_count[s], reverse=True)
print songs_ordered[:3]
# sys.exit(0)





eval = evaluator(500)

u = 0
l = len(user_to_songs)
for user in user_to_songs:
	
	#Find songs to recommend
	songs_to_recommend = []
	for song in songs_ordered:
		if len(songs_to_recommend) >= 500:
			break
		if not song in user_to_songs[user]:
			songs_to_recommend.append(song)
	
	eval.add_ranking(user, songs_to_recommend)
	
	#print progression
	u += 1
	if u % 1000 == 0 or u == l:
		print u, "/", l, "MAP = ", eval.get_MAP()

print "MAP:", eval.get_MAP()









# f = open('kaggle_users.txt', 'r')
# canonical_users = map(lambda line: line.strip(), f.readlines())
# f.close()




# f = open('kaggle_songs.txt', 'r')
# song_to_index = dict(map(lambda line: line.strip().split(' '), f.readlines()))
# f.close()

# u = 0
# f = open('submission.txt', 'w')
# for user in canonical_users:

	# #print progression
	# u += 1
	# if u % 100 == 0:
		# print u
	
	# #Find songs to recommend
	# songs_to_recommend = []
	# for song in songs_ordered:
		# if len(songs_to_recommend) >= 500:
			# break
		# if not song in user_to_songs[user]:
			# songs_to_recommend.append(song)
	
	# eval.add_ranking(user, songs_to_recommend)
			
	# # Transform song IDs to song indexes
	# indices = map(lambda s: song_to_index[s], songs_to_recommend)
	
	# # Write line for that user
	# f.write(' '.join(indices) + '\n')
# f.close()

	