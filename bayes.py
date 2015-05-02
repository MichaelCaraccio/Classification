__author__ = 'Christophe Bolinhas et Michael Caraccio'

from File import File
import random
import math
from collections import Counter

def splitByClass(dataset):

    iPos = 0
    iNeg = 0
    pos = {}
    neg = {}
    for file in dataset:
        if 'neg' in file:
            neg[file] = dataset[file]
            iNeg += len(neg[file])
        else:
            pos[file] = dataset[file]
            iPos+= len(pos[file])

    return pos, neg, iPos, iNeg

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


def getDataByClass(dataset, pourcentagePos, pourcentageNeg):
    #trainSet, testSet = getSets(dataset, pourcentagePos)
    #posTrainSet, negTrainSet = splitByClass(trainSet)
    #posTestSet, negTestSet = splitByClass(testSet)
    posFiles, negFiles, iPos, iNeg = splitByClass(dataset)
    posTrainSet, posTestSet = getSets(posFiles,pourcentagePos)
    negTrainSet, negTestSet = getSets(negFiles,pourcentageNeg)


    return  posTrainSet, negTrainSet, posTestSet, negTestSet, iPos, iNeg

def generateVector(wordList):
    wordVectors = {}
    for word in wordList:
        wordVectors[word] = 0
    return wordVectors

def normalize(entryLength, wordVectorList):
    for word in wordVectorList:
        wordVectorList[word] /= entryLength+6

def evaluateVectors(classSet, wordVectorList):
    #print(classSet)
    for entry in classSet:
        for word in classSet[entry]:
            if word in wordVectorList.keys():
                wordVectorList[word] += 1
    #normalize(len(wordVectorList),wordVectorList)

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
        #vectorSummary[word]["count"] =
        vectorSummary[word]["mean"] = mean(vectorSet[word], len(dataset))
        vectorSummary[word]["ecartType"] = variance(counterFile, dataset, word, vectorSummary[word]["mean"])

    return vectorSummary

def calculateProbability(x, mean, ecarttype):

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
    return probability


def vectorClassProbability(classVector, entry, iWords):
    proba = 0
    for word in entry:
        if word in classVector.keys():
            #print(classVector["heureux"])
            proba += math.log10(((classVector[word]+1)/(iWords+len(classVector)))**entry[word])
            #if classVector[word]["mean"] != 0:

                #proba += math.log10(classVector[word]["mean"]**entry[word])
                #proba += calculateProbability(entry[word],classVector[word]["mean"], classVector[word]["ecartType"])
    return proba
import time
if __name__ == "__main__":

    startTime = time.time()

    print("Classification de mots utilisant Bayes")
    print("-----------------------------------------------------\n")

    fileManager = File()
    #wordList = fileManager.from_folder()
    wordList = fileManager.from_tagged_folder()
    fileList = fileManager.fileContentList


    lightdisplay = True
    # Arguments


    print("Split positif | Split négatif | Erreur positifs | Erreur négatif | Erreur moyenne")
    for pi in range(10,95 , 5):

        pourcentagePos = pi/100.0 #meilleur 0.5 / 0.8
        pourcentageNeg = pi/100.0

        startTime = time.time()

        #print("Répartition des corpus par class : %.2f positifs et %.2f négatifs" % (pourcentagePos*100, pourcentageNeg*100))

        if not lightdisplay:
            print("\n-----------------------------------------------------")
            print("Séparation en corpus d'entrainement et de test")
            print("-----------------------------------------------------\n")


        posTrainSet, negTrainSet, posTestSet, negTestSet, iPos, iNeg = getDataByClass(fileList, pourcentagePos, pourcentageNeg)
        if not lightdisplay:
            print("Corpus d'entrainement : %d" % (len(posTrainSet)+len(negTrainSet)))
            print("Corpus de test : %d" % (len(posTestSet)+len(negTestSet)))


        if not lightdisplay:
            print("Génération du modèle de vecteur")
            print("-----------------------------------------------------")
        baseVector = generateVector(wordList)
        if not lightdisplay:
            print("Longueur du vecteur de base (nombre de mots) : %d" % len(baseVector))
            print("\n-----------------------------------------------------")
            print("Comptage des occurences dans les set d'entrainement")
            print("-----------------------------------------------------")
        posVectors = evaluateVectors(posTrainSet, baseVector.copy())
        negVectors = evaluateVectors(negTrainSet, baseVector.copy())
        if not lightdisplay:
            print("temps d'exécution : %.2fs"%(time.time()-startTime))

        if not lightdisplay:
            print("\n-----------------------------------------------------")
            print("Analyse probabilistique du set d'entrainement")
            print("-----------------------------------------------------")
        sumPos = summarizeDataset(posVectors, posTrainSet)
        sumNeg = summarizeDataset(negVectors, negTrainSet)
        if not lightdisplay:
            print("temps d'exécution : %.2fs"%(time.time()-startTime))



        if not lightdisplay:
            print("\n-----------------------------------------------------")
            print("Analyse d'erreur du corpus de test")
            print("-----------------------------------------------------")

        error = 0
        #print(posVectors)
        counterFilePos = {}
        for file in posTestSet:
            counterFilePos[file]= Counter(posTestSet[file])
        counterFileNeg = {}
        for file in negTestSet:
            counterFileNeg[file] = Counter(negTestSet[file])
        for file in counterFilePos:
            posProb = vectorClassProbability(posVectors,counterFilePos[file], iPos)
            negProb = vectorClassProbability(negVectors,counterFilePos[file], iNeg)
            if posProb < negProb:
                error+=1
        tempError = error
        errorPos = error/(len(counterFilePos))

        #print(str(errorPos*100)+ "% d'erreur sur le corpus de test positif")

        for file in counterFileNeg:
            posProb = vectorClassProbability(posVectors,counterFileNeg[file], iPos)
            negProb = vectorClassProbability(negVectors,counterFileNeg[file], iNeg)
            if posProb > negProb:
                error+=1
        errorNeg = (error-tempError)/(len(counterFileNeg))
        #print(str(errorNeg*100)+ "% d'erreur sur le corpus de test négatif")
        if not lightdisplay:
            print("\n-----------------------------------------------------")
        print("%d%%\t%d%%\t%.2f%%\t%.2f%%\t%.2f%%\t%.2f"  % (pourcentagePos*100, pourcentageNeg*100,errorPos*100,errorNeg*100,((errorPos+errorNeg)/2*100),(time.time()-startTime)))


        #print("temps d'exécution : %.2fs"%(time.time()-startTime))


    #print(classProbability(posVectors,sumPos))
    #print("---------")
    #aaprint(sumNeg)