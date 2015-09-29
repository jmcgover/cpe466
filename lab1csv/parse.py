#!/usr/bin/python
from __future__ import print_function

import os
import sys

# Custom files
sys.path.append(os.getcwd())
import document
from document import Document
from vocabulary import Vocabulary

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
        print("Total Words         : %d" % (doc.getNumTotalWords()))
        print("Different Words     : %d" % (doc.getNumDifferentWords()))
        print("Number of Sentences : %d" % (doc.getNumSentences()))
        print("Number of Paragraphs: %d" % (doc.getNumParagraphs()))
        for w in doc:
            print("%s: %s" % (w, doc.getWordCount(w)))
    elif sys.argv[1][-3:] == "csv":
        print("CSV file extenstion.")
        sys.exit(22)
    else:
        print("Bad file extenstion.")
        sys.exit(22)

if __name__ == '__main__':
    main()
