from MEC import bruteF_MEC, welzl
import numpy as np
from time import time
from plot_utils import Plotter
import os

# Test Code
n_runs = 2000
cardinality_range = [6,30]
eps = 1e-3
def within_tolerance(n1, n2):
    return n1 - eps <= n2 <= n1 + eps
def test_centers(mec1, mec2):
    return within_tolerance(mec1[0][0],mec2[0][0]) and within_tolerance(mec1[0][1],mec2[0][1])

def test_radii(mec1, mec2):
    return within_tolerance(mec1[1], mec2[1])

def ok_nok(bool):
    return "OK" if bool else "NOT_OK"

passed = 0
time_bf = []
time_welzl = []


PLOT_FAILS = True
plot_dir = "./saved/failures"
os.makedirs(plot_dir, exist_ok=True)

if PLOT_FAILS:
    plotter = Plotter()
    run_dir = os.path.join(plot_dir,plotter.run_id)
    os.makedirs(run_dir, exist_ok=True)
else:
    plotter = None

for i in range(n_runs):
    n_points = np.random.randint(cardinality_range[0], cardinality_range[1])
    P = np.random.uniform(-10,10, size=(n_points, 2)).tolist()

    start = time()
    mec_bf = bruteF_MEC(P)
    time_bf.append(time() - start)

    start = time()
    mec_welzl = welzl(P)
    time_welzl.append(time() - start)

    identical_centers = test_centers(mec_bf, mec_welzl)
    identical_radii = test_radii(mec_bf, mec_welzl)
    success = identical_centers and identical_radii
    if success:
        passed += 1

    center_ok = ok_nok(identical_centers)
    radius_ok = ok_nok(identical_radii)
    test = "PASS" if success else "FAIL"
    print("[TEST][{}] Center: {}  Radius: {}".format(test, center_ok, radius_ok))
    if (not success) and PLOT_FAILS:
        print('bf;r:{};c:{}'.format(np.round(mec_bf[1],2), np.round(mec_bf[0],2)))
        print('wel;r:{};c:{}'.format(np.round(mec_welzl[1],2), np.round(mec_welzl[0],2)))
        plotter.set_P(P).plot_circle(mec_bf, color='g', alpha=0.5)
        plotter.plot_circle(mec_welzl, color='r', alpha=0.5)
        plotter.save(os.path.join(run_dir, "case_{}.png".format(str(i).zfill(6))))

failed = n_runs - passed
print("#"*10)
print("\nPassed: {}, Failed: {}, Total: {}".format(passed, failed, n_runs))
print("\nAverage times:")
print("\tBrute force: {}ms, Welzl: {}ms".format(np.mean(time_bf).round(6)*1000, np.mean(time_welzl).round(6)*1000))
