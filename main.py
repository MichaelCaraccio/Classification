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


    #Creation du système de Neurones
    finalNeuron = Neurone()
    m = 1   #Nombre de colonne cachées
    n = 15  #Nombre de neurones par colonne
    alpha = 0.001 #Alpha
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

    iterCount = 1
    error =10
    minError = 6
    while error > minError and iterCount > 0:
        error = 0
        iterCount-=1
        for file in fileManager.fileContentList:
            print("------------ NEW FILE HANDLE " + file + "-----------")
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
            target = 0
            target += 'pos' in file

            currentErr = finalNeuron.calculateErr(target)    #currentErr = err(finalNeuron.getValue(),target)
            if currentErr > alpha:
                print("FIXING DAT SHIT YO")
                error += 1
                #Forward d'abord sur le final
                for neuro in finalNeuron.previousNeuros:
                    deltaWeight = alpha * currentErr * neuro.getValue()
                    neuro.calibrateWeight(finalNeuron, deltaWeight)
                finalNeuron.calculateIntraWeight()
                #Puis sur chaque colonne, colonne par colonne    fin -> début
                for col in intermediateNeurons:
                    print("col Handling")
                    for neuro in col:
                        print("Handling Neurone")
                        errValue = 0
                        #On récupère l'erreur par rapport à tous ses neurones forward
                        for nextNeuro in neuro.weightToNeuroList:
                            errValue += neuro.weightToNeuroList[nextNeuro] * nextNeuro.localErr
                        neuro.localErr = dsigmoid(neuro.getValue())*errValue
                        print("Error calcultated")
                        for previousNeuro in neuro.previousNeuros:
                            deltaWeight = alpha * neuro.localErr * neuro.getValue()
                            previousNeuro.calibrateWeight(neuro, deltaWeight)
                        neuro.calculateIntraWeight()
                        print("Intra Weight redifined")
