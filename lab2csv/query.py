#! /usr/bin/python

# CPE 466 Fall 2015
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

from __future__ import print_function

import os
import re
import sys
import math

import stemming
from stemming import PorterStemmer

# Custom files
sys.path.append(os.getcwd())
import utterance
from utterance import Vocabulary
from utterance import Utterance
import bisect
import operator

# QUERY
class Query(object):
    def __init__(self):
        self.vocab = Vocabulary()
        self.vector = ''
        self.results = {}

    def __iter__(self):
        return self.vocab.__iter__()

    def addWord(self, word):
        self.vocab.add(word)

    def getWordCount(self, word):
        return self.vocab.getWordCount(word)

    def getWordList(self):
        return self.vocab.getWordList()



# DELIMITERS
DELIM_SENT = "\.|!|\?"

DELIM_WORD =  "\s+"                 # White Space
DELIM_WORD += "%s|%s" % ("|,|:|;|\(|\)", DELIM_SENT)        # Punctuation
# DELIM_WORD += "|,|:|;|\(|\)"        # Punctuation
DELIM_WORD += "|\s-+\s"             # Non-Hyphen Dashes
# DELIM_WORD += "|(\s+|^)'|'(\s+|$)|^'(\s+)"  # Single Quotation
DELIM_WORD += "|\""                 # Double Quotation
DELIM_WORD += "|\.{3}"              # Ellipses



regexSent = re.compile(DELIM_SENT)
regexWord = re.compile(DELIM_WORD)
def isEmpty(str):
    if str:
        str.strip()
    return not (str == "" or str == None)

# QUERY PARSER
class QueryParser(object):
    def __init__(self, file, utterances):
        self.file = file
        self.query = Query()
        self.utterances = utterances
        self.stem = utterances.stem
        self.stopwords = utterances.stopwords
        self.stopwordList = utterances.stopwordList
#        self.vocab = Vocabulary()
#        print('Building a parser!') #TODO REMOVE

    def generateWeights(self):
        words = self.utterances.vocab.getWordList()
#        print(words)
        for w in words:
            wordCount = self.query.getWordCount(w)
            if self.query.vector != '':
                self.query.vector += ','
            if wordCount == 0:
                self.query.vector += '0'
            else:
                idf = math.log(self.utterances.count/float(self.utterances.getWordCount(w)),2)
                weight = wordCount * idf
                self.query.vector += str(weight)

    def parseQuery(self):
        if self.utterances.stem == True:
            stemmer = PorterStemmer()
        for line in self.file:
            if line != "\n":
                line = line.strip()
                punctMarks = regexSent.findall(line)
                sentences = regexSent.split(line)
                sentences = filter(None, sentences)
                for s in sentences:
                    s = s.strip()
                    words = regexWord.split(s)
                    words = filter(None, words)
                    for w in words:
                        w = w.lower()
                        w = w.strip("'").strip('-')
                        newWord = ''
                        if w and w not in self.stopwordList:
                            if self.utterances.stem == True and w.isalpha():
                                newWord += stemmer.stem(w,0,len(w)-1)
                            else:
                                newWord += w
                            self.query.addWord(newWord)
        # debug prints!!!
  #      print(self.query.getWordList())
        print("Generating query term weights...")
        self.generateWeights()
        print("Done!")

        return None

