__author__ = 'juust'


import numpy as np
import math
from math import pow
from Point import Point
from File import File
from Neurone import Neurone
from eval import dsigmoid




def resetEntries(wordNeuro):
    for neuro in wordNeuro:
        wordNeuro[neuro].setValue(0)



if __name__ == "__main__":
    print("THIS IS MAIN")
    fileManager = File()
    uniqueWordList = fileManager.from_folder()
    wordNeurons = {}
    intermediateNeurons = []
    percentageGenerate = 0.1

    #Creation du système de Neurones
    finalNeuron = Neurone()
    m = 1   #Nombre de colonne cachées
    n = 10  #Nombre de neurones par colonne
    alpha = 0.1 #Alpha
    threshold = 0.5

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
        wordNeurons[word] = Neurone()

    for neuro in intermediateNeurons[-1]:
        neuro.linkToWords(wordNeurons)

    iterCount = 5
    error =10
    minError = 6

    fileList = list(fileManager.fileContentList)
    splitIdx = int(percentageGenerate*len(fileList))
    fileEval = fileList[:splitIdx]
    fileTest = fileList[splitIdx:]


    while error > minError and iterCount > 0:
        error = 0
        iterCount-=1
        for file in fileEval:
            resetEntries(wordNeurons)
            fileContent = fileManager.fileContentList[file]
            #Active les neurones en fonction du fichier
            for word in fileContent:
                if word in wordNeurons.keys():
                    wordNeurons[word].setValue(wordNeurons[word].getValue()+1.0)
            #On évalue chaque neurone de chaque colonne
            for col in reversed(intermediateNeurons):
                for neuro in col:
                    neuro.calculateValue()
            #On évalue le neuronne final
            finalNeuron.calculateValue()
            target = -1
            target += ('pos' in file)*2


            #print("target : " + str(target) + " | value : " + str(finalNeuron.tempValue))
            if (target > 0 and finalNeuron.tempValue < 0) or (target < 0 and finalNeuron.tempValue > 0):
                #print(file + " : " + str(finalNeuron.tempValue) + " - " + str(target))
                currentErr = finalNeuron.calculateErr(target)
                error += 1
                #Forward d'abord sur le final
                for neuro in finalNeuron.previousNeuros:
                    deltaWeight = alpha * currentErr * neuro.getValue()
                    neuro.calibrateWeight(finalNeuron, deltaWeight)
                finalNeuron.calculateIntraWeight()
                #Puis sur chaque colonne, colonne par colonne    fin -> début
                for col in intermediateNeurons:
                    for neuro in col:
                        errValue = 0
                        #On récupère l'erreur par rapport à tous ses neurones forward
                        for nextNeuro in neuro.weightToNeuroList:
                            errValue += neuro.weightToNeuroList[nextNeuro] * nextNeuro.localErr
                        neuro.localErr = dsigmoid(neuro.getValue())*errValue
                        for previousNeuro in neuro.previousNeuros:
                            deltaWeight = alpha * neuro.localErr * neuro.getValue()
                            previousNeuro.calibrateWeight(neuro, deltaWeight)
                        neuro.calculateIntraWeight()

    errorCount = 0
    for file in fileTest:
            resetEntries(wordNeurons)
            fileContent = fileManager.fileContentList[file]
            #Active les neurones en fonction du fichier
            for word in fileContent:
                if word in wordNeurons.keys():
                    wordNeurons[word].setValue(wordNeurons[word].getValue()+1.0)
            #On évalue chaque neurone de chaque colonne
            for col in reversed(intermediateNeurons):
                for neuro in col:
                    neuro.calculateValue()
            #On évalue le neuronne final
            finalNeuron.calculateValue()
            #print(file + " : " + str(finalNeuron.getValue()))
            target = -1
            target += ('pos' in file)*2



            currentErr = finalNeuron.calculateErr(target)    #currentErr = err(finalNeuron.getValue(),target)
            if (target > 0 and finalNeuron.tempValue < 0) or (target < 0 and finalNeuron.tempValue > 0):
                errorCount+=1
    print(str(errorCount) + " erreurs sur " + str(splitIdx) + " fichiers d'analyse et " + str(len(fileList)-splitIdx))
    print("Réseau interne composé de " + str(m) + " colonnes cachées et " + str(n) + " neuronnes par colonne")
    print("Nombre de réitérations sur les fichiers d'analyse : " + str(iterCount))
    print("Taux d'erreur : "  + str(100-(errorCount/len(fileTest))*100) + "%")