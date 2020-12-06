import numpy as np
from MEC import bruteF_MEC, welzl, welzl_mtf, get_points
from time import time
import matplotlib.pyplot as plt


total_points = 800
inlier_range = (-5,5)

def radial_pertubation(a, fraction, sigma_min, sigma_max):
    a = np.copy(a)
    num_perturbed = int(fraction*len(a))
    indices_pertubed = np.random.randint(0,len(a), num_perturbed)
    for i in indices_pertubed:
        perturb_strength = np.random.uniform(sigma_min, sigma_max)
        a[i] = perturb_strength * a[i]

    return a

def get_runtime_stats(method, P, runs=10):
    times = []
    for _ in range(runs):
        start = time()
        method(P)
        times.append(time()-start)
    return dict(mean=np.mean(times), min=np.min(times), max=np.max(times))


def outlier_test(method, P, fraction_range=(0.5, 25), sigma_min=100, sigma_max=200, step=0.5, runs=50):
    P = P.copy()
    fractions = np.arange(fraction_range[0], fraction_range[1], step)
    fractions = np.linspace(fraction_range[0], fraction_range[1], runs)
    runtimes = {}
    for f in fractions:
        Pdash = radial_pertubation(P, f, sigma_min, sigma_max)
        runtimes[f] = get_runtime_stats(method, Pdash)
    return runtimes


def plot_runtimes(ax, runtimes, label, base_time, **kwargs):
    fractions = list(runtimes.keys())
    means, mins, maxs = zip(*[(v['mean']/base_time['mean'], v['min']/base_time['min'], v['max']/base_time['max']) for v in runtimes.values()])
    ax.plot(fractions, means, label=label, **kwargs)
    ax.fill_between(fractions, mins, maxs, alpha=0.1, **kwargs)


P = np.random.uniform(inlier_range[0], inlier_range[1], (total_points, 2))

no_outlier_time_welzl = get_runtime_stats(welzl, P)
no_outlier_time_welzl_mtf = get_runtime_stats(welzl_mtf, P)

runtimes_welzl = outlier_test(welzl, P)
runtimes_welzlmtf = outlier_test(welzl_mtf, P)


fig, ax = plt.subplots()
plot_runtimes(ax, runtimes_welzl, label='Welzl', base_time=no_outlier_time_welzl)
plot_runtimes(ax, runtimes_welzlmtf, label='WelzlMTF', base_time=no_outlier_time_welzl_mtf)
plt.legend()
plt.show()