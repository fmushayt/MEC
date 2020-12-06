import numpy as np 
import matplotlib.pyplot as plt
from statistics import mean
from numpy import log10 as log
from time import time
from MEC import get_points, bruteF_MEC, welzl

# Generate Points

def get_points(n=10, dist="gaussian", alphaBeta=None, multi=None):
    if dist == "uniform":
        X = np.random.uniform(-10, 10, size=(n, 2))

    elif dist == "gaussian":
        X = np.random.normal(0, 3, size=(n, 2))

    elif dist == "beta":
        X = np.random.beta(alphaBeta[0], alphaBeta[1], size=(n,2))
    
    elif dist == "multivariate":
        X = np.random.multivariate_normal(multi[0], multi[1], size=(n,2))
    
    else:
        pass
    return X


DISTRIBUTIONS = ["unifrom", "gaussian", "beta", "multivariate" ]

vals = {
    "beta": [0.1, 0.1],
    "multivariate": [ [-5, 0, 5], [[1,0,0],[0,1,0],[0,0,1]] ]
}

for dist in DISTRIBUTIONS:
    
