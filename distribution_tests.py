import numpy as np 
from statistics import mean
from numpy import log10 as log
from time import time
from MEC import welzl, welzl_mtf, get_points
import matplotlib.pyplot as plt

DISTRIBUTIONS = ["uniform", "gaussian", "beta", "multi" ]

vals = {
    "beta": [ [0.1, 0.1] ],
    "multi": [ [2, None], [10, None], [20, None] ]
}

fig, axs = plt.subplots(6, 2, figsize=(10, 15))

i = 0
for dist in DISTRIBUTIONS:
    
    configs = []
    if dist == "beta" or dist == "multi":
        configs = vals[dist]
    else:
        configs = [None]
    
    for config in configs:

        welzl_times = {}
        mtf_times = {}

        P = []
        for n in range(20, 500):

            print("Simlating for " + dist + " for n = " + str(n))

            for trial in range(10):
    
                P = get_points(n=n, dist=dist, params=config)


                start = time()
                welzl(P)
                welzlT = time() - start

                start = time()
                welzl_mtf(P)
                mtfT = time() - start

                if trial == 0:
                    welzl_times[n] = [welzlT]
                    mtf_times[n] = [mtfT]
                else: 
                    welzl_times[n].append(welzlT)
                    mtf_times[n].append(mtfT)


        P = np.array(P)
        axs[i, 0].scatter(P[:,0], P[:,1])

        wl = np.array([ [log(mean(l)), log(min(l)), log(max(l))] for l in welzl_times.values()])
        mtf = np.array([ [log(mean(l)), log(min(l)), log(max(l))] for l in mtf_times.values()])

        axs[i, 1].plot(welzl_times.keys(), wl[:,0], color="yellow", label="Vanilla Welzl")
        axs[i, 1].fill_between(welzl_times.keys(), wl[:,1], wl[:,2], color="yellow", alpha=.1)
        axs[i, 1].plot(mtf_times.keys(), mtf[:,0], color="blue", label="MTF Welzls")
        axs[i, 1].fill_between(mtf_times.keys(), mtf[:,1], mtf[:,2], color="blue", alpha=.1)
        if i == 0:
            axs[i, 1].legend()

        i += 1


axs[0, 0].set_title('Distributions')
axs[0, 1].set_title('Runtimes')

ax = axs.flat
ax[0].set(ylabel = "Uniform")
ax[2].set(ylabel = "Gaussian")
ax[4].set(ylabel = "Beta")
ax[6].set(ylabel = "Multimodal k = 2")
ax[8].set(ylabel = "Multimodal k = 10")
ax[10].set(ylabel = "Multimodal k = 20")


'''
j = 0
ks = ["3","5","8"]
for ax in axs.flat:
    print(j)
    label = DISTRIBUTIONS[min(j, 3)]
    if j >= 3:
        label += "modal k = " + ks[j%3]
    ax.set(ylabel=label)
    j += 1
'''

fig.suptitle('Effect of distribution on Welzl (log secs scale)')
fig.savefig("Distributions on Welzl")

print("Distribution testing on welzl Complete!")




