# -*- coding: utf-8 -*-
__author__ = 'michaelcaraccio'

import os
import re
import csv

class File:

    def __init__(self):
        self.filesContent = []
        self.frenchST = self.initFrenchST()
        self.filesContentUnique = []
        self.filesMerged = []
        self.folders = ["pos", "neg"]
        self.taggedFolders = ["tagged/pos", "tagged/neg"]
        self.fileContentList = {}

    # -----------------------------------------------------------
    # Get words from tagged folder
    # -----------------------------------------------------------
    def from_tagged_folder(self):
        for folder in self.taggedFolders:
            for file in os.listdir(folder):
                if file.endswith(".txt"):
                    self.fileContentList[file] = self.wordFromFileWithDelimiter(folder+"/"+file,'\t')
                    # Get all words from file and Store them in an array
                    self.filesContent.append(self.fileContentList[file])
        self.mergeList()
        self.unique()
        self.clean()
        return self.filesMerged

    # -----------------------------------------------------------
    # Get words from pos and get folder at root folder
    # -----------------------------------------------------------
    def from_folder(self):
        for folder in self.folders:
            for file in os.listdir(folder):
                if file.endswith(".txt"):
                    self.fileContentList[file] = self.wordFromFile(folder+"/"+file)
                    # Get all words from file and Store them in an array
                    self.filesContent.append(self.fileContentList[file])

                    #self.wordFromFileWithDelimiter('tagged/neg/neg-0520.txt', '\t')
        self.mergeList()
        self.unique()
        self.clean()
        return self.filesMerged


    def mergeList(self):
        for sentences in self.filesContent:
            for words in sentences:
                self.filesMerged.append(words)

    def unique(self):
        self.filesMerged = list(set(self.filesMerged))

    def clean(self):
        for words in self.filesMerged:
            if words in self.frenchST:
                self.filesMerged.remove(words)

    def wordFromFile(self, filename):
        return re.findall(r'\w+', open(filename,'r',encoding='utf-8').read())

    def initFrenchST(self):
        return re.findall(r'\w+', open("frenchST.txt",'r',encoding='utf-8').read())

    def wordFromFileWithDelimiter(self, filename, delimite):
        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter=delimite)
            listword = []
            for row in reader:
                try:
                    listword.append(row[2])
                except:
                    print("delimiter faux")

            return listword