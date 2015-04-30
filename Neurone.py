from random import uniform
from eval import sigmoid, err

class Neurone:
    def __init__(self):
        self.weightToNeuroList = {}
        self.previousNeuros = []
        self.valueOutput = 0
        self.intraWeight = uniform(-1,1)
        self.lastWeight = {}
        self.deltaWeight = {}

    def getSum(self, neuro):
        return neuro.valueOutput * neuro.weightToNeuroList[self]

    def getValue(self):
        return self.valueOutput

    def calculateErr(self, target):
        self.localErr = err(self.valueOutput,target)
        return self.localErr

    def calculateValue(self):
        self.valueOutput = self.intraWeight
        for neuro in self.previousNeuros:
            self.valueOutput += self.getSum(neuro)
        self.setValue(sigmoid(self.valueOutput))

    def setValue(self, value):
        self.valueOutput = value

    def getWeight(self, neuro):
        return self.weightToNeuroList[neuro]

    def setWeight(self, neuro, weight):
        self.weightToNeuroList[neuro] = weight


    def calibrateWeight(self, neuro, deltaW):
        self.lastWeight[neuro] = self.weightToNeuroList[neuro]
        self.deltaWeight[neuro] = deltaW
        self.weightToNeuroList[neuro] += deltaW

    def calculateIntraWeight(self):
        for neuro in self.previousNeuros:
            self.intraWeight += self.localErr

    def initNeuro(self, neuroList):
        for neuro in neuroList:
            self.previousNeuros.append(neuro)
            neuro.setWeight(self,uniform(-1,1))

    def linkToWords(self, wordList):
        for word in wordList:
            self.previousNeuros.append(wordList[word])
            wordList[word].setWeight(self, uniform(-1,1))