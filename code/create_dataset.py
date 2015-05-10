import sys
import random
import os

ds_name = sys.argv[1]
n_users = int(sys.argv[2])
min_hist = int(sys.argv[3])
max_hist = int(sys.argv[4])

users = set()
songs = set()
u2i = {}
f = open('datasets/train_triplets.txt', 'r')
i = 0
for line in f:
	i += 1
	if i % 1000000 == 0:
		print i
	user, song, count = line.strip().split('\t')
	
	if user not in u2i:
		u2i[user] = {}
	u2i[user][song] = count
f.close()

users_min_hist = [u for u in u2i if min_hist <= len(u2i[u]) <= max_hist]
kaggle_users = random.sample(users_min_hist, n_users)

kaggle_songs = set()
dirname = "datasets/" + ds_name + "/"
filename = dirname + ds_name + ".txt"
os.makedirs(dirname)
f = open(filename, 'w')
for user in kaggle_users:
	for song in u2i[user]:
		kaggle_songs.add(song)
		f.write('\t'.join([user, song, count]) + '\n')
f.close()
kaggle_songs = list(kaggle_songs)


kaggle_users = sorted(kaggle_users)
f = open(dirname + "kaggle_users.txt", 'w')
for user in kaggle_users:
	f.write(user + "\n")
f.close()


kaggle_songs = sorted(kaggle_songs)
f = open(dirname + "kaggle_songs.txt", 'w')
for idx, song in enumerate(kaggle_songs):
	f.write(song + " " + str(idx+ 1) + "\n")
f.close()

