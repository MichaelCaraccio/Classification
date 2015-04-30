from random import uniform


class Neurone:
    def __init__(self):
        self.weightToNeuroList = {}
        self.previousNeuros = []
        self.valueOutput = 0


    def getSum(self, neuro):
        return neuro.valueOutput * neuro.weightToNeuroList[self]

    def getValue(self):
        return self.valueOutput

    def calculateValue(self):
        self.valueOutput = 0
        for neuro in self.previousNeuros:
            self.valueOutput += self.getSum(neuro)

    def setValue(self, value):
        self.valueOutput = value

    def getWeight(self, neuro):
        return self.weightToNeuroList[neuro]

    def setWeight(self, neuro, weight):
        self.weightToNeuroList[neuro] = weight


    def initNeuro(self, neuroList):
        for neuro in neuroList:
            self.previousNeuros.append(neuro)
            neuro.setWeight(self,uniform(-1,1))

    def linkToWords(self, wordList):
        for word in wordList:
            self.previousNeuros.append(wordList[word])
            wordList[word].setWeight(self, uniform(-1,1))