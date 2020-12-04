import numpy as np 
import matplotlib.pyplot as plt
from statistics import mean
from time import time
from MEC import get_points, bruteF_MEC, welzl

bruteF_times = {}
welzl_times = {}

bruteF_Timeout = False  # Flag to decide whether to stop brute force tests or not
T = 10 ** 5 # Threshold for bruteforce cutoff
maxN = 100


for n in range(3, maxN):
    
    print("Testing for n = " + str(n))

    for trial in range(10):
    
        P = get_points(n, dist="uniform")

        start = time()
        welzl(P)
        welzlT = time() - start

        if trial == 0:
            welzl_times[n] = [welzlT]
        else: welzl_times[n].append(welzlT)

        if not bruteF_Timeout:
            start = time()
            bruteF_MEC(P)
            bruteT = time() - start

            if trial == 0:
                bruteF_times[n] = [bruteT]
            else: bruteF_times[n].append(bruteT)

        if not bruteF_Timeout and bruteT > T * welzlT:
            print("Brute Force timed out at n = " + str(n))
            print("Welzl took " + str(welzlT) + " while Brute Force took " + str(bruteT))
            bruteF_Timeout = True

print("Runtime Testing Complete!")

bf = np.array([ [mean(l), min(l), max(l)] for l in bruteF_times.values()])
wl = np.array([ [mean(l), min(l), max(l)] for l in welzl_times.values()])
 

plt.plot(bruteF_times.keys(), bf[:,0], color="red", label="Brute Force")
plt.fill_between(bruteF_times.keys(), bf[:,1], bf[:,2], color="red", alpha=.1)
plt.plot(welzl_times.keys(), wl[:,0], color="#FFD700", label="Welzls")
plt.fill_between(welzl_times.keys(), wl[:,1], wl[:,2], color="#FFD700", alpha=.1)
plt.xlabel("#Points (n)")
plt.ylabel("Runtime of Algorithm (seconds)")
plt.title("Runtime by number of points")
plt.legend()
plt.show()    










