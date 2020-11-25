import numpy as np 
import matplotlib.pyplot as plt
import miniball as M
from MEC import *

s = np.random.randn(100,2)

C, r2 = M.get_bounding_ball(s)

cir = bruteF_MEC(s)

circle1 = plt.Circle(C, r2, color='r')
circle2 = plt.Circle(cir[0], cir[1], color='blue')

fig, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot
# (or if you have an existing figure)
# fig = plt.gcf()
# ax = fig.gca()

ax.add_artist(circle1)
ax.add_artist(circle2)

fig.savefig('plotcircles.png')