__author__ = 'Christophe Bolinhas et Michael Caraccio'

from File import File

def getWords():
    fileManager = File()
    return fileManager.from_folder()

def handleData():
    listWords = getWords()



if __name__ == "__main__":

    print("\n-----------------------------------------------------")
    print("Classification de mots utilisant un réseau de neurone")
    print("-----------------------------------------------------\n")


