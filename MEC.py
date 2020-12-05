import numpy as np
from math import sqrt
import random

infinity = float('inf')


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
    D = bx * cy - by * cx  #TODO : Handle the case when D = 0. When and why does that happen?
    return [(cy * B - by * C) / (2 * D),
            (bx * C - cx * B) / (2 * D)]


# Find MEC using Brute Force approach

def bruteF_MEC(P):
    # Number of points in set P
    n = len(P)

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

            # Check if circle is smaller than previous ones, as well as if it encloses all points
            if circle[1] < mec[1] and enclosing(circle, P):
                mec = circle

    # Find MEC by trying all triplets
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):

                # Get circle defined by points pi and pj
                circle = findCircle([P[i], P[j], P[k]])

                # Check if circle is smaller than previous ones, as well as if it encloses all points
                if circle[1] < mec[1] and enclosing(circle, P):
                    mec = circle

    return mec


######################################################################################################


# Find MEC using Welzl's algorithm

def welzl(P):
    # Create a shuffled copy of the set of points and run welzls recursive algo on it
    P_copy = P.copy()
    random.shuffle(P_copy)
    result = welzlR(P_copy, [])
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
    circle = welzlR(P, R)
    if within(circle, p): return circle
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
            return circle

        for i in range(n):
            if not within(circle, self.P[i]):
                circle = self.run(i, R+[self.P[i]])
                # move pi to front
                p = self.P[i]
                del self.P[i]
                self.P.insert(0,p)

        return circle

def welzl_mtf(P):
    return WelzlMTF(P).run(len(P), [])

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

def rep_circle(circle):
    return "Center: ({},{}), Radius: {}".format(circle[0][0], circle[0][1], circle[1])

# # Test Code
# #
# a =   [ [ 0, 0 ],
#                                 [ 0, 1 ],
#                                 [ 1, 0 ] ]
#
# mec1 = bruteF_MEC(a)
# mec2 = welzl(a)
# mecmtf = welzl_mtf(a)
#
# print("Brute F Center = { ",mec1[0][1],",",mec1[0][1],
#                 "} Radius = ",round(mec1[1],6))
#
# print("Welzl Center = { ",mec2[0][1],",",mec2[0][1],
#                 "} Radius = ",round(mec2[1],6))
# print("MTF: {}".format(rep_circle(mecmtf)))
# b = [[5, -2],
#      [-3, -2],
#      [-2, 5],
#      [1, 6],
#      [0, 2]]
#
# mec3 = bruteF_MEC(b)
# mec4 = welzl(b)
# mecmtf = welzl_mtf(b)
# print("Brute F Center = {", mec3[0][0], ",", mec3[0][1],
#       "} Radius = ", mec3[1])
#
# print("Welzl Center = {", mec4[0][0], ",", mec4[0][1],
#       "} Radius = ", mec4[1])
# print("MTF: {}".format(rep_circle(mecmtf)))
#
# num_points = 5
# b = np.random.uniform(-6,6, size=(num_points,2)).tolist()
#
# mec3 = bruteF_MEC(b)
# mec4 = welzl(b)
# mecmtf = welzl_mtf(b)
# print("Brute F Center = {", mec3[0][0], ",", mec3[0][1],
#       "} Radius = ", mec3[1])
#
# print("Welzl Center = {", mec4[0][0], ",", mec4[0][1],
#       "} Radius = ", mec4[1])
# print("MTF: {}".format(rep_circle(mecmtf)))