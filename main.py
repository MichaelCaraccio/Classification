__author__ = 'Christophe Bolinhas et Michael Caraccio'

from File import File
from Neurone import Neurone
from eval import dsigmoid
import time

def resetEntries(wordNeuro):
    for neuro in wordNeuro:
        wordNeuro[neuro].setValue(0)

def resetRelations(col):
    for neuro in col:
        neuro.isRelatedToWords = False


def evaluate(fileManager, file, wordNeurons, intermediateNeurons,finalNeuron):
    resetEntries(wordNeurons)
    fileContent = fileManager.fileContentList[file]
    listWordFileNeurons = []
    listWordFileNeurons.clear()
    resetRelations(intermediateNeurons[-1])
    # Active les neurones en fonction du fichier
    for word in fileContent:
        if word in wordNeurons.keys():
            wordNeurons[word].setValue(wordNeurons[word].getValue() + 1.0)

            if wordNeurons[word] not in listWordFileNeurons:
                listWordFileNeurons.append(wordNeurons[word])
    for neuro in intermediateNeurons[-1]:
        neuro.setRelatedToWords(listWordFileNeurons)

    #On évalue chaque neurone de chaque colonne
    for col in reversed(intermediateNeurons):
        for neuro in col:
            neuro.calculateValue()

    #On évalue le neuronne final
    finalNeuron.calculateValue()
    #print(finalNeuron.getValue())


if __name__ == "__main__":

    # Arguments
    m = 1                    # Nombre de colonne cachées
    n = 15                    # Nombre de neurones par colonne
    alpha = 0.1             # Alpha
    iterCount = 3            # Nombre d'itération
    percentageGenerate = 0.2 # Pourcentage de corpus d'entrainement
    threshold = 0.05

    start_time = time.time()
    print("\n-----------------------------------------------------")
    print("Classification de mots utilisant un réseau de neurone")
    print("-----------------------------------------------------\n")

    fileManager = File()
    uniqueWordList = fileManager.from_folder()
    wordNeurons = {}
    intermediateNeurons = []
    print("Arguments :")
    print("\tNombre de réitérations sur les fichiers d'analyse : " + str(iterCount))
    print("\tRéseau interne composé de " + str(m) + " colonnes cachées et " + str(n) + " neuronnes par colonne")
    print("\tAlpha %.2f\n" % alpha)


    print("Lecture des fichiers : %f seconds" % (time.time() - start_time))

    #Creation du système de Neurones
    finalNeuron = Neurone()

    for x in range(0, m):
        listCol = []
        for y in range(0, n):
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

    print("Réseau créé : %f secondes" % (time.time() - start_time))

    fileList = list(fileManager.fileContentList)
    splitIdx = int(percentageGenerate*len(fileList))
    fileEval = fileList[:splitIdx]
    fileTest = fileList[splitIdx:]

    print("Découpage du corpus d'entrainement en %d fichiers : %f secondes" % (splitIdx, (time.time() - start_time)))

    lastFileChecked = None
    allOk = False

    while not allOk and iterCount > 0:
        print("Reste %d : %f secondes" % (iterCount, (time.time() - start_time)))
        iterCount -= 1
        for file in fileEval:
            #if file is lastFileChecked:
            #    allOk = True
            #    break
            lastFileChecked = file

            evaluate(fileManager, file, wordNeurons, intermediateNeurons,finalNeuron)

            target = -1
            target += ('pos' in file) * 2


            if (target > 0 > finalNeuron.tempValue) or (target < 0 < finalNeuron.tempValue):
                currentErr = finalNeuron.calculateErr(target)

                while currentErr > threshold:
                    currentErr = finalNeuron.calculateErr(target)

                    #print(finalNeuron.tempValue)

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
                            #errValue /= len(neuro.weightToNeuroList)

                            neuro.localErr = dsigmoid(neuro.getValue()) * errValue
                            #print(neuro.localErr)
                            if neuro.isRelatedToWords:
                                for previousNeuro in neuro.listWords:
                                    deltaWeight = alpha * neuro.localErr * neuro.getValue()
                                    previousNeuro.calibrateWeight(neuro, deltaWeight)
                            else:
                                for previousNeuro in neuro.previousNeuros:
                                    deltaWeight = alpha * neuro.localErr * neuro.getValue()
                                    previousNeuro.calibrateWeight(neuro, deltaWeight)

                            #print("----------------")
                            #print(neuro.intraWeight)
                            neuro.calculateIntraWeight()

                    evaluate(fileManager, file, wordNeurons, intermediateNeurons,finalNeuron)

                            #print(neuro.intraWeight)

    print("Découpage du corpus de test en %d fichiers en %f secondes" % (len(fileTest), (time.time() - start_time)))

    errorCount = 0
    for file in fileTest:
        # resetEntries(wordNeurons)
        # fileContent = fileManager.fileContentList[file]
        # listWordFileNeurons = []
        # listWordFileNeurons.clear()
        #
        # resetRelations(intermediateNeurons[-1])
        #
        #
        # #Active les neurones en fonction du fichier
        # for word in fileContent:
        #     if word in wordNeurons.keys():
        #         wordNeurons[word].setValue(wordNeurons[word].getValue() + 1.0)
        #
        #         if wordNeurons[word] not in listWordFileNeurons:
        #             listWordFileNeurons.append(wordNeurons[word])
        #
        # for neuro in intermediateNeurons[-1]:
        #     neuro.setRelatedToWords(listWordFileNeurons)
        #
        # #On évalue chaque neurone de chaque colonne
        # for col in reversed(intermediateNeurons):
        #     for neuro in col:
        #         neuro.calculateValue()
        #         #print(neuro.getValue())
        #
        # #On évalue le neuronne final
        # finalNeuron.calculateValue()
        evaluate(fileManager, file, wordNeurons, intermediateNeurons,finalNeuron)

        target = -1
        target += ('pos' in file) * 2

        currentErr = finalNeuron.calculateErr(target)
        #print(file)
        #print(finalNeuron.tempValue)
        #print(finalNeuron.getValue())
        #print("------")

        if (target > 0 > finalNeuron.tempValue) or (target < 0 < finalNeuron.tempValue):
            errorCount+=1



    print(str(errorCount) + " erreurs sur " + str(splitIdx) + " fichiers d'entrainement et " + str(len(fileList)-splitIdx) + " fichiers de tests")
    print("Taux de réussite : "  + str(100-(errorCount/len(fileTest))*100) + "%")
    print("Temps total d'execution : %f secondes" % (time.time() - start_time))