import numpy as np
from MEC import bruteF_MEC, welzl, welzl_mtf, get_points
from time import time
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

total_points = 100

def get_runtime_stats(method, P, runs=10):
    times = []
    for _ in range(runs):
        start = time()
        method(P)
        times.append(time()-start)
    return dict(mean=np.mean(times), min=np.min(times), max=np.max(times))

def plot_runtimes(ax, runtimes, label, normalize=False, **kwargs):
    x = list(runtimes.keys())
    means, mins, maxs = zip(*[(v['mean'], v['min'], v['max']) for v in runtimes.values()])
    means, mins, maxs = np.asarray(means), np.asarray(mins), np.asarray(maxs)
    if normalize:
        means = means/means.max()
        mins = mins/mins.max()
        maxs = maxs/maxs.max()
    # ax.plot(x, means, c="#FFD700", label=label, **kwargs)
    # ax.fill_between(x, mins, maxs, facecolor="#FFD700", alpha=0.1, **kwargs)
    ax.plot(x, means, c="r", label=label, **kwargs)
    ax.fill_between(x, mins, maxs, facecolor="r", alpha=0.1, **kwargs)

def plot_order_four(ax, domain, C_range=(0.8e-8,8e-8), **kwargs):
    y = np.asarray(domain)**4
    lower = C_range[0]*y
    upper = C_range[1]*y
    ax.plot(domain, lower, c='orange', marker='o', markersize=3.5, label='0.1cn^4',**kwargs)
    ax.plot(domain, upper, c='orange', marker='s', markersize=3.5, label='cn^4',**kwargs)
    ax.fill_between(domain, lower, upper, alpha=0.1, facecolor='orange', **kwargs)


def plot_order_one(ax, domain, C_range=(0.8e-5,8e-5), **kwargs):
    y = np.asarray(domain)
    lower = C_range[0]*y
    upper = C_range[1]*y
    ax.plot(domain, lower, c='orange', marker='o', markersize=3.5, label='0.1cn',**kwargs)
    ax.plot(domain, upper, c='orange', marker='s', markersize=3.5, label='cn',**kwargs)
    ax.fill_between(domain, lower, upper, alpha=0.1, facecolor='orange', **kwargs)



def f(x, c):
    return c*x

P = get_points(total_points)

N = np.asarray(range(3, len(P)))
runtimes_bf = {}
# base = get_runtime_stats(bruteF_MEC, P, runs=1)
for i in N:
    runtimes_bf[i] = get_runtime_stats(bruteF_MEC, P[:i], runs=1)

means = np.asarray([v['mean'] for v in runtimes_bf.values()])
# means = means/means.max()
# print(curve_fit(f, N, means, [2e-8]))

fig, ax = plt.subplots()
plot_runtimes(ax, runtimes_bf, label='Brute Force')
plot_order_four(ax, N[::3])
plt.xlabel("Number of points (N)")
plt.ylabel("Time (s)")
plt.legend()
plt.show()


# N = np.asarray(range(3, len(P)))
# runtimes_welzl = {}
# # base = get_runtime_stats(bruteF_MEC, P, runs=1)
# for i in N:
#     runtimes_welzl[i] = get_runtime_stats(welzl, P[:i], runs=10)
#
# means = np.asarray([v['mean'] for v in runtimes_welzl.values()])
# # means = means/means.max()
# print(curve_fit(f, N, means, [1]))
#
# fig, ax = plt.subplots()
# plot_runtimes(ax, runtimes_welzl, label='Welzl')
# plot_order_one(ax, N[::3])
# plt.xlabel("Number of points (N)")
# plt.ylabel("Time (s)")
# plt.legend()
# plt.show()