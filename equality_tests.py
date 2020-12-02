from MEC import bruteF_MEC, welzl
import numpy as np
from time import time
# Test Code
n_runs = 100
cardinality_range = [6,30]

def test_centers(mec1, mec2):
    return mec1[0][0] == mec2[0][0] and mec1[0][1] == mec2[0][1]

def test_radii(mec1, mec2):
    return mec1[1] == mec2[1]

def ok_nok(bool):
    return "OK" if bool else "NOT_OK"

passed = 0
time_bf = []
time_welzl = []
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
    if identical_centers and identical_radii:
        passed += 1

    center_ok = ok_nok(identical_centers)
    radius_ok = ok_nok(identical_radii)
    test = "PASS" if identical_centers and identical_radii else "FAIL"
    print("[TEST][{}] Center: {}  Radius: {}".format(test, center_ok, radius_ok))

failed = n_runs - passed
print("#"*10)
print("\nPassed: {}, Failed: {}, Total: {}".format(passed, failed, n_runs))
print("\nAverage times:")
print("\tBrute force: {}ms, Welzl: {}ms".format(np.mean(time_bf).round(6)*1000, np.mean(time_welzl).round(6)*1000))
