__author__ = 'Christophe Bolinhas & Michael Caraccio'

from math import exp


def s(xTab, wTab, x0):
	value = 0;
	for x, w in zip(xTab, wTab):
		value += x*w
	return value

def y(s):
	return 1/(1+exp(-s))


def err(y, yCorrect):
	return y*(1-y)*(yCorrect-y)