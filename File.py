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


    def from_folder(self):
        for folder in self.folders:
            for file in os.listdir(folder):
                if file.endswith(".txt"):

                    # Get all words from file and Store them in an array
                    self.filesContent.append(self.wordFromFile(folder+"/"+file))

                    #self.wordFromFileWithDelimiter('tagged/neg/neg-0520.txt', '\t')
        self.mergeList()
        self.unique()
        self.clean()
        return self.filesMerged


    def mergeList(self):
        for sentences in self.filesContent:
            for words in sentences:
                self.filesMerged.append(words)
        print(len(self.filesMerged))

    def unique(self):
        self.filesMerged = list(set(self.filesMerged))
        print(len(self.filesMerged))

    def clean(self):
        for words in self.filesMerged:
            if words in self.frenchST:
                self.filesMerged.remove(words)
        print(len(self.filesMerged))

    def wordFromFile(self, filename):
        #print(filename)
        return re.findall(r'\w+', open(filename,'r',encoding='utf-8').read())

    def initFrenchST(self):
        return re.findall(r'\w+', open("frenchST.txt",'r',encoding='utf-8').read())

    def wordFromFileWithDelimiter(self, filename, delimite):
        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter=delimite)
            for row in reader:
                print(row)