__author__ = 'juust'


import numpy as np
import math
from math import pow
from Point import Point
from File import File
from Neurone import Neurone




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


    for file in fileManager.fileContentList:
        fileContent = fileManager.fileContentList[file]
        #Active les neurones en fonction du fichier
        for word in fileContent:
            if word in wordNeurons.keys():
                wordNeurons[word].setValue(wordNeurons[word].getValue()+1.0)
        #On selectionne la premiüre colonne de neuronnes cachös
        firstCol = intermediateNeurons[-1]
        for col in intermediateNeurons:
            for neuro in col:
                neuro.calculateValue()
                print(neuro.getValue())
            print("----")
        finalNeuron.calculateValue()
        print(finalNeuron.getValue())

        break



