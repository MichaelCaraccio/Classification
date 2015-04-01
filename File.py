__author__ = 'michaelcaraccio'

import os

class File:

    def __init__(self, path):
       self._path = path

    def from_file(self):
        for file in os.listdir(self._path):
            if file.endswith(".txt"):
                reader = open(self._path+"/"+file, 'r')
                print(reader.read())