# Use this file only for demonstration and animations
# Use MEC.py for core logic and experiments
from collections import Counter

import numpy as np
from math import sqrt
import random
import matplotlib.pyplot as plt
from plot_utils import AnimatedPlotter

infinity = float('inf')

fps = 15
####################################################################

# Generate Points

def get_points(n=10, dist="gaussian"):
    if dist == "uniform":
        X = np.random.uniform(-10, 10, size=(n, 2))

    elif dist == "gaussian":
        X = np.random.normal(0, 3, size=(n, 2))

    else:
        pass
    return X

def get_clusters(n, k, means=None, dist="gaussian"):
    """ Generates n points sampled from k clusters with (given or random) means"""
    if means is None:
        means = np.random.uniform(-50,50, (k,2))
    else:
        assert len(means) == k, "Number of clusters and means must be same but got {} and {}".format(k, len(means))

    # decide number of points in each cluster by randomly assigning them to each one by one
    indices = list(range(k))  # make sure each cluster has atleast one point
    indices.extend(np.random.choice(list(range(k)), n - k))  # assign the rest randomly to k clusters
    points_per_cluster = Counter(indices)  # count points per cluster
    X = []
    for cluster_idx, n_points_cluster in points_per_cluster.items():
        x = means[cluster_idx] + np.asarray(get_points(n_points_cluster, dist))
        X.extend(x.tolist())
    return X

####################################################################


# Euclidean distance

def dist(p, q):
    return sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Check if point is withtin a circle
# Circle = [centerPoint, radius]


def within(circle, p):
    return dist(circle[0], p) <= circle[1] + 1e-4  # small tolerance value

# Check if circle encloses points

def enclosing(circle, P):
    for p in P:
        if not within(circle, p): return False
    return True


# Define circle from 2 or 3 points

def findCircle(points):
    n = len(points)
    p1 = points[0]
    p2 = points[1]

    if n == 2:
        center = [(p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0]
        radius = dist(center, p1)
        circle = [center, radius]

    elif n == 3:
        p3 = points[2]
        center = findCenter(p2[0] - p1[0], p2[1] - p1[1], p3[0] - p1[0], p3[1] - p1[1])
        center[0] += p1[0]
        center[1] += p1[1]
        radius = dist(center, p1)
        circle = [center, radius]

    else:
        raise ValueError("Only two or three points are supported, but got {}".format(n))
    return circle


# Find center of circle defined by 3 points

def findCenter(bx, by, cx, cy):
    B = bx * bx + by * by
    C = cx * cx + cy * cy
    D = bx * cy - by * cx
    return [(cy * B - by * C) / (2 * D),
            (bx * C - cx * B) / (2 * D)]


# Find MEC using Brute Force approach

def bruteF_MEC(P):
    # Number of points in set P
    n = len(P)
    plotter = AnimatedPlotter(run_id="BruteForce5").set_P(P).plot_P()
    # Return MEC for trivial cases
    if n == 0:
        return [[0, 0], 0]
    if n == 1:
        return [P[0], 0]

    # Define base enclosing circle to be at origin with infinite radius
    mec = [[0, 0], infinity]

    # Find MEC by trying all pairs of points
    for i in range(n):
        for j in range(i + 1, n):

            # Get circle defined by points pi and pj
            circle = findCircle([P[i], P[j]])
            plotter.plot_circle(circle, color='y').dcc()
            # Check if circle is smaller than previous ones, as well as if it encloses all points
            if circle[1] < mec[1] and enclosing(circle, P):
                mec = circle

    # Find MEC by trying all triplets
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):

                # Get circle defined by points pi and pj
                circle = findCircle([P[i], P[j], P[k]])
                plotter.plot_circle(circle, color='y').dcc()
                # Check if circle is smaller than previous ones, as well as if it encloses all points
                if circle[1] < mec[1] and enclosing(circle, P):
                    mec = circle
    plotter.plot_circle(mec, color='g').dcc()
    plotter.save_animation(fps=fps)
    return mec


######################################################################################################


# Find MEC using Welzl's algorithm

plotting = True
plotter = None

def welzl(P):
    global plotter
    # Create a shuffled copy of the set of points and run welzls recursive algo on it
    P_copy = P.copy()
    plotter = AnimatedPlotter(run_id="Welzl5")
    plotter.set_P(P).plot_P()
    random.shuffle(P_copy)
    result = welzlR(P_copy, [])
    plotter.plot_circle(result, color='g').dcc()
    plotter.save_animation(fps=fps)
    return result


def welzlR(P, R):
    n = len(P)

    # If we run out of points or support set is size of 3 return circle from trivial case
    if n == 0 or len(R) == 3:
        return trivial(R)

    idx = random.randint(0, n - 1)
    P = list(P)
    P[idx], P[n - 1] = P[n - 1], P[idx]
    p = P.pop()

    plotter.plot_point(p, c='r')
    circle = welzlR(P, R)
    plotter.plot_circle(circle, color='y').dcc()
    if within(circle, p): return circle
    if len(R) > 0: plotter.plot_points(R, c='orange')
    return welzlR(P, R + [p])


class WelzlMTF:
    def __init__(self, P):
        """Implements move to front heuristic proposed by Welzl"""

        self.P = list(P)  # copy
        random.shuffle(self.P)  # Random permutation


    def run(self, n, R):

        circle = trivial(R)

        # If support set is size of 3 return circle from trivial case
        if len(R) == 3 or n < 0:
            plotter.plot_circle(circle, color='y').dcc()
            return circle

        for i in range(n):
            if not within(circle, self.P[i]):
                plotter.plot_point(self.P[i], c='r')
                if len(R)>0 : plotter.plot_points(R, c='orange')
                circle = self.run(i, R+[self.P[i]])
                plotter.plot_circle(circle, color='y').dcc()
                # move pi to front
                p = self.P[i]
                del self.P[i]
                self.P.insert(0,p)

        return circle


def welzl_mtf(P):
    global plotter
    plotter = AnimatedPlotter(run_id="WelzlMTF5").set_P(P).plot_P()
    circle = WelzlMTF(P).run(len(P), [])
    plotter.plot_circle(circle, color='g').dcc()
    plotter.save_animation(fps=fps)
    return circle




def trivial(R):
    assert len(R) <= 3, "Trivial is defined only on three or lesser points, but got {}".format(len(R))
    # Number of points in set P
    n = len(R)

    # Return MEC for trivial cases
    if n == 0:
        return [[0, 0], 0]
    elif n == 1:
        return [R[0], 0]
    elif n == 2:
        return findCircle(R)
    else:

        # Check if circle can be determined by two points
        for i in range(n):
            for j in range(i + 1, n):

                circle = findCircle([R[i], R[j]])
                if enclosing(circle, R):
                    return circle

        # Otherwise, circle is defined by all three points
        return findCircle(R)

# Test Code

# a =   [ [ 0, 0 ],
#                                 [ 0, 1 ],
#                                 [ 1, 0 ] ]

# mec1 = bruteF_MEC(a)
# mec2 = welzl(a)

# print("Brute F Center = { ",mec1[0][1],",",mec1[0][1],
#                 "} Radius = ",round(mec1[1],6))

# print("Welzl Center = { ",mec2[0][1],",",mec2[0][1],
#                 "} Radius = ",round(mec2[1],6))

b = np.random.randint(-10,10, size=(6, 2)).tolist()
# b = [[5, -2],
#      [-3, -2],
#      [-2, 5],
#      [1, 6],
#      [0, 2]]

mec3 = bruteF_MEC(b)
mec4 = welzl(b)
mec5 = welzl_mtf(b)

print("Brute F Center = {", mec3[0][0], ",", mec3[0][1],
      "} Radius = ", mec3[1])

print("Welzl Center = {", mec4[0][0], ",", mec4[0][1],
      "} Radius = ", mec4[1])

print("Welzl Center = {", mec5[0][0], ",", mec5[0][1],
      "} Radius = ", mec5[1])
