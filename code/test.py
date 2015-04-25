import math
import time

a = [[1.] * 163000] * 110000
b = []

n = 110000
sti=time.clock()
for i in range(n):

	if i % 100 == 0:
		print i,		
		cti=time.clock()-sti
		print " tot secs: %f (%f)"%(cti,cti/(i+1))
		
	for j in range(n):
		a = math.log10(10)
input("d")




# d ={}
# d['a'] = "A"
# d['b'] = "B"
# print len(d)

# import numpy as np
# import matplotlib.pyplot as plt

#evenly sampled time at 200ms intervals
# t = np.arange(0., 5., 0.2)

#red dashes, blue squares and green triangles
# plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'y^', t, t**4, 'g*-')
# plt.show()
