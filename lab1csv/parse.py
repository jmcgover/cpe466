#!/usr/bin/python
from __future__ import print_function

import sys
import os

# Custom files
sys.path.append(os.getcwd())
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
    if sys.argv[1][-3:] != "txt":
        print("Bad file extenstion.")
        sys.exit(22)
    file = open(sys.argv[1], 'r')
    lines = file.readlines()
    file.close()
    paragraphCount = 0
    for line in lines:
        if line == '\n':
            print("Found a new line!")
            paragraphCount += 1
    if paragraphCount:
        paragraphCount += 1
    print("Paragraph Count: %d" % (paragraphCount))
    doc = Document()
    vocab = Vocabulary()
    vocab.add('fuck')
    vocab.add('fuck')
    vocab.add('fuck')
    vocab.add('fuck')
    vocab.add('fuck')
    vocab.add('fuck')
    vocab.add('shit')
    vocab.add('shit')
    vocab.add('shit')
    vocab.add('muh')
    vocab.add('muh')
    vocab.add('muh')
    vocab.add('muh')
    vocab.add('muh')
    vocab.add('muh')
    vocab.add('muh')
    vocab.add('muh')
    vocab.add('muh')
    vocab.add('muh')
    for w in vocab:
        print("%s: %d" % (w, vocab.getWordCount(w)))
    return 0

if __name__ == '__main__':
    main()
