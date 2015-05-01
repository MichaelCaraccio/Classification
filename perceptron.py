__author__ = 'Christophe Bolinhas et Michael Caraccio'

def deltaClasses(alpha, erreur, src):
    return alpha*erreur*src

def calculateWeight(deltaClass, oldWeight):
    return deltaClass+oldWeight

def ek(d, y):
    return d-y

def deltaK(y, ek):
    return y*(1-y)*ek

def erreurSortie(yPrime, ek):
    return ek*yPrime

def erreurCouche(yPrime, wTab, eTab):
    sum = 0
    for e, w in zip(eTab, wTab):
        sum += e*w
    return sum

