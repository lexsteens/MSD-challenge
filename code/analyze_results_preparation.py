from dataset import dataset
import numpy as np
import matplotlib.pyplot as plt
import sys

ds_name = sys.argv[1]
dir_name = "datasets/%s"%(ds_name)

dataset_ts = dataset("%s_ts.txt"%(ds_name))
u2i = dataset_ts.user_item_matrix['binary']
i2u = dataset_ts.item_user_matrix['binary']

users = sorted(u2i.keys())
items = sorted(i2u.keys())

f = open("%s/user_history_lengths.txt"%(dir_name), 'w')
for user in users:
	f.write("%d %d\n" % (user, len(u2i[user])))
f.close()

f = open("%s/item_listening_lengths.txt"%(dir_name), 'w')
for item in items:
	f.write("%d %d\n" % (item, len(i2u[item])))
f.close()