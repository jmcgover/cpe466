#!/usr/bin/python

# CPE 466 Fall 2015
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

from __future__ import print_function

import os
import sys

# Custom files
sys.path.append(os.getcwd())
import document
from document import Document
from vocabulary import Vocabulary
import custom_csv
from custom_csv import Custom_CSV

def main():

    # Initial input checking
    if len(sys.argv) < 2:
        print("Insufficient arguments. Usage: parse.py <fileName>")
        sys.exit(22)
    if os.path.isfile(sys.argv[1]) == False:
        print("File does not exist.")
        sys.exit(22)
    if sys.argv[1][-3:] == "txt":
        doc = Document()
        with open(sys.argv[1]) as file:
            parser = document.Parser(file, doc)
            parser.parseDocument()
 #       for w in doc:
 #           print("%s: %s" % (w, doc.getWordCount(w)))
        if len(sys.argv) >= 3:
            if "-stats" in sys.argv:
                print("Document Statistics:")
                print("Total Words         : %d" % (doc.getNumTotalWords()))
                print("Different Words     : %d" % (doc.getNumDifferentWords()))
                print("Number of Sentences : %d" % (doc.getNumSentences()))
                print("Number of Paragraphs: %d" % (doc.getNumParagraphs()))
                print("------------")
            if "-lw" in sys.argv:
                print("Words in Document:")
                for w in doc:
                    print("%s" % (w))
                print("------------")
            if "-lwf" in sys.argv:
                print("Word Frequency in Document:")
                for w in doc:
                    print("%s: %s" % (w, doc.getWordCount(w)))
                print("------------")
            if "-mfw" in sys.argv:
                print("Most Frequent Word(s) in Document:")
                maxFreq = 0
                mostFreqWords = []
                for w in doc:
                    if doc.getWordCount(w) > maxFreq:
                        maxFreq = doc.getWordCount(w)
                        mostFreqWords = []
                        mostFreqWords.append(w)
                    elif doc.getWordCount(w) == maxFreq:
                        mostFreqWords.append(w)
                for w in mostFreqWords:
                    print("%s: %s" % (w, maxFreq))
                print("------------")
            for args in sys.argv:
                if "-find=" in args:
                    searchWord = args[6:]
                    if len(searchWord) > 0:
                        print("Searching for Word \"%s\" in Document:" % searchWord)
                        print("%s: %s" % (searchWord, doc.getWordCount(searchWord)))
                        print("------------")
    elif sys.argv[1][-3:] == "csv":
        csv = Custom_CSV()
        with open(sys.argv[1]) as file:
            parser = custom_csv.CSV_Parser(file, csv)
            parser.parseCSV()
    else:
        print("Bad file extenstion.")
        sys.exit(22)

if __name__ == '__main__':
    main()
