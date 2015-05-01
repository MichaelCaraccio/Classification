__author__ = 'Christophe Bolinhas et Michael Caraccio'

from File import File
import random
import math
from collections import Counter

def splitByClass(dataset):


    pos = {}
    neg = {}
    for file in dataset:
        if 'neg' in file:
            neg[file] = dataset[file]
        else:
            pos[file] = dataset[file]
    return pos, neg

def mean(instances, fileCount):
    return instances/float(fileCount)


def variance(counterFile, dataset, word, meanWord):

    #meanWord = mean(instances, len(dataset))
    variance = 0

    for counter in counterFile:
        variance += (counterFile[counter][word]-meanWord)**2
    variance /= float(len(dataset)-1)
    return math.sqrt(variance)

def getSets(dataset, pourcentage):
    splitSize = int(len(dataset)*pourcentage)
    evalSet = {}

    listEntries= dataset.copy()
    keyList = list(listEntries.keys())

    while len(evalSet) < splitSize:
        idx = random.randrange(len(keyList))
        key = keyList.pop(idx)
        evalSet[key] = listEntries.pop(key)
    return evalSet, listEntries


def getDataByClass(dataset, pourcentage):
    trainSet, testSet = getSets(dataset, pourcentage)
    posTrainSet, negTrainSet = splitByClass(trainSet)
    posTestSet, negTestSet = splitByClass(testSet)
    return  posTrainSet, negTrainSet, posTestSet, negTestSet

def generateVector(wordList):
    wordVectors = {}
    for word in wordList:
        wordVectors[word] = 0
    return wordVectors

def normalize(entryLength, wordVectorList):
    for word in wordVectorList:
        wordVectorList[word] /= entryLength

def evaluateVectors(classSet, wordVectorList):
    #print(classSet)
    for entry in classSet:
        for word in classSet[entry]:
            if word in wordVectorList.keys():
                wordVectorList[word] += 1
    #normalize(len(classSet),wordVectorList)

    return wordVectorList

def displayVector(wordVectorList):
    for word in wordVectorList:
        if wordVectorList[word] != 0:
            print("%s:%f" % (word, wordVectorList[word]))

def summarizeDataset(vectorSet, dataset):

    vectorSummary = {}
    counterFile = {}

    for file in dataset:
        counterFile[file]= Counter(dataset[file])

    for word in vectorSet:
        vectorSummary[word] = {}
        vectorSummary[word]["mean"] = mean(vectorSet[word], len(dataset))
        vectorSummary[word]["ecartType"] = variance(counterFile, dataset, word, vectorSummary[word]["mean"])

    return vectorSummary

def calculateProbability(x, mean, ecarttype, nbWords):

    if x == 0 or mean == 0 or ecarttype == 0:
        return 1
    exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(ecarttype,2))))
    return (1 / (math.sqrt(2*math.pi) * ecarttype)) * exponent

def classProbability(vectorSet, vectorSummary):
    probability = 1

    for word in vectorSummary:
        meanWord, ecartType = vectorSummary[word]["mean"], vectorSummary[word]["ecartType"]
        val = vectorSet[word]
        probability *= calculateProbability(val, meanWord, ecartType)
        print(probability)
        if probability == 0:
            print(val)
            print(meanWord)
            print(ecartType)
            print(word)
            break
    return probability

if __name__ == "__main__":

    print("\n-----------------------------------------------------")
    print("Classification de mots utilisant Bayes")
    print("-----------------------------------------------------\n")

    fileManager = File()
    wordList = fileManager.from_folder()
    fileList = fileManager.fileContentList

    # Arguments
    pourcentage = 0.7

    posTrainSet, negTrainSet, posTestSet, negTestSet = getDataByClass(fileList, pourcentage)
    baseVector = generateVector(wordList)
    posVectors = evaluateVectors(posTrainSet, baseVector.copy())
    negVectors = evaluateVectors(negTrainSet, baseVector.copy())

    sumPos = summarizeDataset(posVectors, posTrainSet)
    #sumNeg = summarizeDataset(negVectors, negTrainSet)


    print(classProbability(posVectors,sumPos))
    print("---------")
    #aaprint(sumNeg)