# -*- coding: latin-1 -*-
__author__ = 'michaelcaraccio'

import numpy as np
import math
from math import pow
from Point import Point
from File import File
from Neurone import Neurone




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

    uniqueWordList = File().from_folder()
    wordNeurons = {}
    intermediateNeurons = []

    finalNeuron = Neurone()
    m = 1   #Nombre de colonne cachées
    n = 15  #Nombre de neurones par colonne

    for x in range(0,m):
        listCol = []
        for y in range(0,n):
            listCol.append(Neurone())
        if x == 0:
            finalNeuron.initNeuro(listCol)
        else:
            for neuro in intermediateNeurons[x-1]:
                neuro.initNeuro(listCol)
        intermediateNeurons.append(listCol)

    for word in uniqueWordList:
        wordNeurons[word] = Neurone



