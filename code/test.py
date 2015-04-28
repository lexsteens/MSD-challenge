#!/usr/bin/env python
import numpy as np
import pylab as P

#
# The hist() function now has a lot more options
#

#
# first create a single histogram
#
mu, sigma = 200, 25
x = mu + sigma*P.randn(10000)



# the histogram of the data with histtype='step'
n, bins, patches = P.hist(x, normed=1, histtype='bar', rwidth=0.8)

P.figure()
bins = [100,125,150,160,170,180,190,200,210,220,230,240,250,275,300]
n, bins, patches = P.hist(x, bins, normed=1, histtype='bar', rwidth=0.8)


P.show()





# import math
# import time

# a = [[1.] * 163000] * 110000
# b = []

# n = 110000
# sti=time.clock()
# for i in range(n):

	# if i % 100 == 0:
		# print i,		
		# cti=time.clock()-sti
		# print " tot secs: %f (%f)"%(cti,cti/(i+1))
		
	# for j in range(n):
		# a = math.log10(10)
# input("d")




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
