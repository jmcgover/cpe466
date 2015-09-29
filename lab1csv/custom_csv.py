#! /usr/bin/python

import os
import re
import sys

# Custom files
sys.path.append(os.getcwd())

# CUSTOM_CSV
class Custom_CSV(object):
    def __init__(self):
        self.vectorCount = 0

    def getNumVectors(self):
        return self.vectorCount

# CSV_PARSER
class CSV_Parser(object):
    def __init__(self, file, Custom_CSV):
        self.file = file
        self.csv = Custom_CSV
        self.vectors = []

    def parseCSV(self):
        for line in self.file:
            line = re.sub("\s+","",line)
            if len(line) != 0:
                if line[0] == ',': # null for first value
                    line = '0' + line
                line = line.replace(",,",",0,") # null in middle of vector
                line = line.replace(",\n",",0\n") # null for last value
#                print(line)
                values = line.split(",") # returns a list of words
                for index, item in enumerate(values):
                    values[index] = float(item)
#                print(values)
                self.vectors.append(values)

        print(self.vectors)

