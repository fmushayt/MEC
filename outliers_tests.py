import numpy as np
from MEC import bruteF_MEC, welzl, welzl_mtf, get_points
from time import time
import matplotlib.pyplot as plt

n_base = 450
total_points = 500
inlier_range = (-5,5)

def radial_pertubation(a,sigma_min=2, sigma_max=5,fraction=None, start_index=None):
    a = np.copy(a)
    if fraction is not None:
        num_perturbed = int(fraction*len(a))
        indices_pertubed = np.random.randint(0,len(a), num_perturbed)
    elif start_index is not None:
        indices_pertubed = list(range(start_index, len(a)))
    else:
        raise ValueError("One of fraction or start_index must be given. But got None")
    for i in indices_pertubed:
        perturb_strength = np.random.uniform(sigma_min, sigma_max)
        # perturb_strength = 2
        a[i] = perturb_strength * a[i]

    return a

def get_runtime_stats(method, P, runs=10):
    times = []
    for _ in range(runs):
        start = time()
        method(P)
        times.append(time()-start)
    return dict(mean=np.mean(times), min=np.min(times), max=np.max(times))


def outlier_test(method, P, fraction_range=(0, 0.05), sigma_min=100, sigma_max=200, runs=50):
    P = P.copy()
    # fractions = np.arange(fraction_range[0], fraction_range[1], step)
    fractions = np.linspace(fraction_range[0], fraction_range[1], runs)
    runtimes = {}
    for f in fractions:
        Pdash = radial_pertubation(P, f, sigma_min, sigma_max)
        runtimes[f] = get_runtime_stats(method, Pdash.tolist())
    return runtimes


def plot_runtimes(ax, runtimes, label, **kwargs):
    x = list(runtimes.keys())
    means, mins, maxs = zip(*[(v['mean'], v['min'], v['max']) for v in runtimes.values()])
    ax.plot(x, means, label=label, **kwargs)
    ax.fill_between(x, mins, maxs, alpha=0.1, **kwargs)

def get_runtime_growth(method, P, start_index=3, step_size=3):
    runtimes = {}
    for i in range(start_index, len(P), step_size):
        runtimes[i] = get_runtime_stats(method, P[:i].copy())
    return runtimes

def relative_runtimes(runtimes, relative_to):
    return {k:{k1:v1/relative_to[k1] for k1,v1 in v.items()} for k,v in runtimes.items()}

# P = np.random.uniform(inlier_range[0], inlier_range[1], (total_points, 2))


P = np.random.randn(total_points, 2)
# base_runtime = get_runtime_stats(welzl, P[:n_base].copy())
runtime_welzl_inliers = get_runtime_growth(welzl, P, start_index=0)
Pdash = radial_pertubation(P.copy(),start_index=n_base)
runtime_welzl_outliers = get_runtime_growth(welzl, Pdash, start_index=n_base)

# rruntime_welzl_outliers = relative_runtimes(runtime_welzl_outliers, base_runtime)
# runtime_welzl_inliers = relative_runtimes(runtime_welzl_inliers, base_runtime)


# no_outlier_time_welzl = get_runtime_stats(welzl, P)
# no_outlier_time_welzl_mtf = get_runtime_stats(welzl_mtf, P)
#
# runtimes_welzl = outlier_test(welzl, P)
# runtimes_welzlmtf = outlier_test(welzl_mtf, P)
#
# # print(runtimes_welzl)
# fig, ax = plt.subplots()
# # plot_runtimes(ax, runtimes_welzl, label='Welzl')
# plot_runtimes(ax, runtimes_welzlmtf, label='WelzlMTF')
# plt.legend()
# plt.show()

# plt.scatter(P[:,0], P[:,1])
# Pdash = radial_pertubation(P, 0.1, 2, 5)
# plt.scatter(Pdash[:,0],Pdash[:,1])
# plt.show()


fig, ax = plt.subplots()
plot_runtimes(ax, runtime_welzl_inliers, label='Welzl-inliers')
plot_runtimes(ax, runtime_welzl_outliers, label='Welzl-outliers')
plt.legend()
plt.show()
