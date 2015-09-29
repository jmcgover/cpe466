#! /usr/bin/python

# CPE 466 Fall 2015
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import os
import re
import sys

# Custom files
sys.path.append(os.getcwd())

# CUSTOM_CSV
class Custom_CSV(object):
    def __init__(self):
        self.vectorCount = 0
        self.vectors = []

    def __iter__(self):
        return self.vectors.__iter__()

    def getNumVectors(self):
        return len(self.vectors)
    def getVector(self, i):
        return self.vectors[i]
    def getVectors(self):
        return self.vectors
    def addVector(self, v):
        self.vectors.append(v)
    def getColumn(self, col):
        column = []
        for v in self.vectors:
            if col < len(v):
                column.append(v[col])
        return column

# CSV_PARSER
class CSV_Parser(object):
    def __init__(self, file, Custom_CSV):
        self.file = file
        self.csv = Custom_CSV

    def parseCSV(self):
        for line in self.file:
            line = re.sub("\s+","",line)
            if len(line) != 0:
                if line[0] == ',':                  # null for first value
                    line = '0' + line
                line = line.replace(",,",",0,")     # null in middle of vector
                line = line.replace(",\n",",0\n")   # null for last value
                values = line.split(",")            # returns a list of words
                for index, item in enumerate(values):
                    try:
                        values[index] = float(item)
                    except ValueError as e:
                        values[index] = 0

                self.csv.addVector(values)
