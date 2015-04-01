__author__ = 'michaelcaraccio'

import numpy as np
import math
from math import pow
from Point import Point
from File import File

def euclidean(x, y):
    return np.linalg.norm(x-y)

def minkowski_distance(px, py, p=2):
    """
    Calculates the minkowski distance between two points.

    PARAMETERS
      x - the first point
      y - the second point
      p - the order of the minkowski algorithm.
          Default = 2. This is equal to the euclidian distance.
                       If the order is 1, it is equal to the manhatten
                       distance.
                       The higher the order, the closer it converges to the
                       Chebyshev distance, which has p=infinity
    """

    return math.sqrt(((abs(px.x - py.x)**2 + (px.y - py.y) **2 )**p) **(1/p))

if __name__ == '__main__':

    a = 2
    b = 8
    print(euclidean(a,b))
    #print(minkowski_distance(a,b))

    a = np.array([ 1, 1, 1])
    b = np.array([ 2, 4, 1])
    print(euclidean(a,b))

    p = Point(1, 1)
    q = Point(1, 4)
    print(minkowski_distance(p,q))

    file = File("pos").from_file()