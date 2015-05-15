from dataset import dataset
import numpy as np
import matplotlib.pyplot as plt

dataset_ts = dataset('sample_1_ts.txt')
u2i = dataset_ts.user_item_matrix['binary']
i2u = dataset_ts.item_user_matrix['binary']

users = sorted(u2i.keys())
items = sorted(i2u.keys())

f = open('datasets/sample_1/user_history_lengths.txt', 'w')
for user in users:
	f.write("%d %d\n" % (user, len(u2i[user])))
f.close()

f = open('datasets/sample_1/item_listening_lengths.txt', 'w')
for item in items:
	f.write("%d %d\n" % (item, len(i2u[item])))
f.close()