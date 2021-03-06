__author__ = 'Christophe Bolinhas et Michael Caraccio'

import numpy as np


def s(xTab, wTab, x0):
	value = 0;
	for x, w in zip(xTab, wTab):
		value += x*w
	return value


def err(y, yCorrect):
	return y*(1-y)*(yCorrect-y)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Derivative sigmoid
def dsigmoid(y):
    return y * (1.0 - y)
