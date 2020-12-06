import numpy as np 
import matplotlib.pyplot as plt
from statistics import mean
from numpy import log10 as log
from time import time
from MEC import welzl, welzl_mtf
import sys

# Generate Points

def get_points(n=10, dist="gaussian", params=None):
    X = []
    print(dist)
    if dist == "uniform":
        X = np.random.uniform(-10, 10, size=(n, 2))
    elif dist == "gaussian":
        X = np.random.normal(0, 3, size=(n, 2))
    elif dist == "beta":
        X = np.random.beta(params[0], params[1], size=(n,2))
    elif dist == "multivariate":
        X = np.random.multivariate_normal(params[0], params[1], size=(n,2))
    else: pass
    return X


DISTRIBUTIONS = ["unifrom", "gaussian", "beta", "multivariate" ]

vals = {
    "beta": [ [0.1, 0.1] ],
    "multivariate": [ [ [-5, 0, 5], [[1,0,0],[0,1,0],[0,0,1]] ] ]
}

dist_times = {}

for dist in DISTRIBUTIONS:
    
    configs = []
    if dist == "beta" or dist == "multivariate":
        configs = vals[dist]
    else:
        configs = [None]
    
    for config in configs:

        welzl_times = {}
        mtf_times = {}

        for n in range(3, 10):
            for trial in range(10):

                P = get_points(n=n, dist=dist, params=config)

                try:
                    start = time()
                    welzl(P)
                    welzlT = time() - start
                except:
                    print(P)
                    print(len(P))
                    print(len(P[0])) 
                    sys.exit(0)


                start = time()
                welzl_mtf(P)
                mtfT = time() - start

                if trial == 0:
                    welzl_times[n] = [welzlT]
                    mtf_times[n] = [mtfT]
                else: 
                    welzl_times[n].append(welzlT)
                    mtf_times[n].append(mtfT)
        
        wl = np.array([ [mean(l), min(l), max(l)] for l in welzl_times.values()])
        mtf = np.array([ [mean(l), min(l), max(l)] for l in mtf_times.values()])

        plt.plot(welzl_times.keys(), wl[:,0], color="yellow", label="Vanilla Welzl")
        plt.fill_between(welzl_times.keys(), wl[:,1], wl[:,2], color="yellow", alpha=.1)
        plt.plot(mtf_times.keys(), mtf[:,0], color="blue", label="MTF Welzls")
        plt.fill_between(mtf_times.keys(), mtf[:,1], mtf[:,2], color="blue", alpha=.1)
        plt.xlabel("#Points (n)")
        plt.ylabel("Runtime of Algorithm (seconds)")
        plt.title("Runtime by number of points")
        plt.legend()

        #plt.savefig("RuntimeComparison.png")
        plt.show()    
        plt.clf()


print("Distribution testing on welzl Complete!")




