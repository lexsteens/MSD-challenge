import numpy as np
import matplotlib.pyplot as plt


song_to_count = {}

song_listening_distribution = [0] * 1000
song_listening_min = 99999999
song_listening_max = 0
song_listening_avg = 0.

f = open('kaggle_visible_evaluation_triplets_ts.txt', 'r')
user_to_songs = {}
triplets = []
for line in f:
	user, song, count = line.strip().split('\t')
	triplets.append((user, song, count))
	
	
	
	c = int(count)
	if c < song_listening_min:
		song_listening_min = c
	if c > song_listening_max:
		song_listening_max = c
	song_listening_avg += c
	song_listening_distribution[c] += 1
	
	if user in user_to_songs:
		user_to_songs[user].add(song)
	else:
		user_to_songs[user] = set([song])
		
	if song in song_to_count:
		song_to_count[song] += 1
	else:
		song_to_count[song] = 1
f.close()
song_listening_avg = song_listening_avg / 1450933

print "Song listening:"
print "----------------"
print song_listening_min
print song_listening_max
print song_listening_avg
print len(user_to_songs)

axis1 = []
for idx, val in enumerate(song_listening_distribution):
	if idx <= 200:
		print idx, '\t', val
	axis1.append(idx)
	
plt.plot(axis1[:200], song_listening_distribution[:200], 'g-')
plt.yscale('log', nonposy='clip')
plt.show()



song_popularity_distribution = [0] * 5044
song_popularity_min = 999999999
song_popularity_max = 0
song_popularity_avg = 0.
song_popularity_total = 0
song_popularity_above_100 = 0
for key in song_to_count:
	song_popularity_distribution[song_to_count[key]] += 1
	song_popularity_total += 1
	if song_to_count[key] >= 200:
		song_popularity_above_100 += 1
	if song_to_count[key] < song_popularity_min:
		song_popularity_min = song_to_count[key]
	if song_to_count[key] > song_popularity_max:
		song_popularity_max = song_to_count[key]
	song_popularity_avg += song_to_count[key]
song_popularity_avg /= len(song_to_count)

print "Song popularity:"
print "----------------"
axis3 = []
for idx, val in enumerate(song_popularity_distribution):
	if idx <= 200:
	#if val != 0:
		print idx, '\t', val
	axis3.append(idx)


print song_popularity_min
print song_popularity_max
print song_popularity_avg
print song_popularity_total
print len(song_to_count)
print song_popularity_above_100
	
plt.plot(axis3[:200], song_popularity_distribution[:200], 'r--')
plt.yscale('log', nonposy='clip')
plt.show()
	



user_type_distribution = [0] * 54
user_type_min = 99999999
user_type_max = 0
user_type_avg = 0.
for user in user_to_songs:
	n = len(user_to_songs[user])
	user_type_distribution[n] += 1
	if n < user_type_min:
		user_type_min = n
	if n > user_type_max:
		user_type_max = n
	user_type_avg += n
user_type_avg = user_type_avg / len(user_to_songs)

print "User type:"
print "----------"
print user_type_min
print user_type_max
print user_type_avg
print len(user_to_songs)

axis = []
for idx, val in enumerate(user_type_distribution):
	print idx, '\t',val
	axis.append(idx)

	
plt.plot(axis, user_type_distribution, 'bo')
plt.yscale('log', nonposy='clip')
plt.show()
