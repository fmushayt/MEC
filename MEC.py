import numpy as np
from math import sqrt
import random

infinity = float('inf')



####################################################################

# Generate Points

def get_points(n=10, dist="gaussian"):

    if dist == "uniform":
        X = np.random.uniform(-10, 10, size=(n,2))

    elif dist == "gaussian":
        X = np.random.normal(0, 3, size=(n,2))

    else:
        pass 
    return X

####################################################################


# Euclidean distance

def dist(p, q):
    return sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2) 


# Check if point is withtin a circle
# Circle = [centerPoint, radius]

def within(circle, p):
    return dist(circle[0], p) <= circle[1]

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
        center = [ (p1[0] + p2[0]) / 2.0 , (p1[1] + p2[1]) / 2.0  ]
        radius = dist(center,p1) 
        circle = [center, radius]

    elif n == 3:
        p3 = points[2]
        center = findCenter(p2[0] - p1[0], p2[1] - p1[1], p3[0] - p1[0], p3[1] - p1[1])
        center[0] += p1[0]
        center[1] += p1[1]
        radius = dist(center, p1)
        circle = [center, radius]

    else: pass
    return circle

# Find center of circle defined by 3 points

def findCenter(bx, by, cx, cy): 
    B = bx * bx + by * by 
    C = cx * cx + cy * cy 
    D = bx * cy - by * cx 
    return [(cy * B - by * C) // (2 * D), 
            (bx * C - cx * B) // (2 * D) ] 


# Find MEC using Brute Force approach

def bruteF_MEC(P):

    # Number of points in set P
    n = len(P)

    # Return MEC for trivial cases
    if n == 0:
        return [[0,0], 0]
    if n == 1:
        return [P[0], 0]

    
    # Define base enclosing circle to be at origin with infinite radius
    mec = [[0,0], infinity]
    
    # Find MEC by trying all pairs of points
    for i in range(n):
        for j in range(i+1, n):

            # Get circle defined by points pi and pj
            circle = findCircle([ P[i], P[j] ])

            # Check if circle is smaller than previous ones, as well as if it encloses all points
            if circle[1] < mec[1] and enclosing(circle, P):
                mec = circle

    # Find MEC by trying all triplets
    for i in range(n):
        for j in range(i+1, n):
            for k in range (j+1, n):

                # Get circle defined by points pi and pj
                circle = findCircle([ P[i], P[j], P[k] ])

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
    return welzlR(P_copy, [])


def welzlR(P, R):

    n = len(P)
    
    # If we run out of points or support set is size of 3 return circle from trivial case
    if n == 0 or len(R) == 3: 
        #print(n)
        #print(R)
        return trivial(R)

    idx = random.randint(0, n-1) 
    P[idx], P[n-1] = P[n-1], P[idx]
    p = P.pop()

    #print(P, p)
    circle = welzlR(P, R)

    if within(circle, p): return circle

    R.append(p)
    return welzlR(P, R)
    



def trivial(R):

    # Number of points in set P
    n = len(R)

    # Return MEC for trivial cases
    if n == 0:
        return [[0,0], 0]
    elif n == 1:
        return [R[0], 0]
    elif n == 2:
        return findCircle(R)
    else:
        
        # Check if circle can be determined by two points
        for i in range(n):
            for j in range(i+1, n):
                
                circle = findCircle([ R[i], R[j] ])
                if enclosing(circle, R):
                    return circle
        
        # Otherwise, circle is defined by all three points
        return findCircle(R)




# Test Code 
  
a =   [ [ 0, 0 ], 
                                [ 0, 1 ], 
                                [ 1, 0 ] ]

mec1 = bruteF_MEC(a)
mec2 = welzl(a)
  
print("Brute F Center = { ",mec1[0][1],",",mec1[0][1], 
                "} Radius = ",round(mec1[1],6)) 

print("Welzl Center = { ",mec2[0][1],",",mec2[0][1], 
                "} Radius = ",round(mec2[1],6)) 
  
b = [ [ 5, -2 ], 
                                [ -3, -2 ], 
                                [ -2, 5 ], 
                                [ 1, 6 ], 
                                [ 0, 2 ] ]
  

mec3 = bruteF_MEC(b)
mec4 = welzl(b)

print("Brute F Center = {",mec3[0][0],",",mec3[0][1], 
        "} Radius = ",mec3[1]) 

print("Welzl Center = {",mec4[0][0],",",mec4[0][1], 
        "} Radius = ",mec4[1]) 
 

