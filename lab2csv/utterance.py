#! /usr/bin/python

# CPE 466 Fall 2015
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

from __future__ import print_function

import os
import re
import sys
import json

import stemming
from stemming import PorterStemmer

# Custom files
sys.path.append(os.getcwd())
import bisect
import operator

class Vocabulary(object):
    def __init__(self):
        self.vocab = {}
        self.wordList = []
        self.totalWords = 0
#        print('Made a blank vocabulary!') #TODO REMOVE

    def __iter__(self):
        return self.wordList.__iter__()

    def add(self, word):
        if word not in self.vocab:
            self.vocab[word] = 0
            bisect.insort(self.wordList, word)
        self.vocab[word] += 1
        self.totalWords += 1

    def getWordCount(self, word):
        if word in self.vocab:
            return self.vocab[word]
        else:
            return 0

    def getNumTotalWords(self):
        return self.totalWords

    def getNumDifferentWords(self):
        return len(self.wordList)

    def getWordList(self):
        return self.wordList


# UTTERANCE
class Utterance(object):
#    def __init__(self, pid, first, last, personType, date, house, committee, text):
    def __init__(self, pid, first, last, personType, text):
        self.vocab = Vocabulary()
        self.pid = pid
        self.first = first
        self.last = last
        self.personType = personType
#        self.date = date
#        self.house = house
#        self.committee = committee
        self.text = text

    def __iter__(self):
        return self.vocab.__iter__()

    def addWord(self, word):
        self.vocab.add(word)

    def getWordCount(self, word):
        return self.vocab.getWordCount(word)

    def getNumTotalWords(self):
        return self.vocab.getNumTotalWords()

    def getNumDifferentWords(self):
        return self.vocab.getNumDifferentWords()

    def compareUtterances(self, other):
        if self.pid == otherUtter.pid:
           if self.text == other.text:
              return True
        return False

# UTTERANCE COLLECTION
class UtteranceCollection(object):
    def __init__(self):
        self.vocab = Vocabulary()
        self.utterances = []
        self.count = 0
        self.stem = False
        self.stopwords = ''
        self.stopwordList = []
        self.pickleFile = "SB277_Processed"

    def __iter__(self):
        return self.vocab.__iter__()

    def addWord(self, word):
        self.vocab.add(word)

    def getWordCount(self, word):
        return self.vocab.getWordCount(word)

    def getNumTotalWords(self):
        return self.vocab.getNumTotalWords()

    def getNumDifferentWords(self):
        return self.vocab.getNumDifferentWords()

    def addUtterance(self, utter):
        if utter not in self.utterances:
            bisect.insort(self.utterances, utter)
            self.count += 1

    def getNumTotalUtterances(self):
        return len(self.utterances)

    def printAllWordsFreq(self):
        words = self.vocab.getWordList()
        print(words)
        for w in words:
            print("%s: %d" % (w , self.vocab.getWordCount(w)))



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

# PARSER
class Parser(object):
    def __init__(self, file, stem, stopwords, utterances):
        self.file = file
        self.utterances = utterances
        self.utterances.stem = stem
        self.utterances.stopwords = stopwords
        self.utterances.stopwordList = []
        self.utterances.pickleFile = "SB277_Processed"
#        self.vocab = Vocabulary()
        print('Building a parser!') #TODO REMOVE

    def parseUtterance(self):
        if self.utterances.stopwords != '':
            try:
               with open(self.utterances.stopwords) as stopword_file:
                  print('Processing stopword file: %s' % (self.utterances.stopwords))
                  for line in stopword_file:
                      line = line.strip()
                      line = line.lower()
                      self.utterances.stopwordList.append(line)
            except FileNotFoundError as e:
               print('Could not find file %s' % (self.utterances.stopwords))
               return e.errno
        data = json.load(self.file)
        if self.utterances.stem == True:
            stemmer = PorterStemmer()
        for item in data:
            newUtter = Utterance(item["pid"], item["first"], item["last"], item["PersonType"], item["text"])
            line = item["text"]

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
                        if w and w not in self.utterances.stopwordList:
                            if self.utterances.stem == True and w.isalpha():
                                newWord += stemmer.stem(w,0,len(w)-1)
                            else:
                               newWord += w
                            newUtter.addWord(newWord)
                            self.utterances.addWord(newWord)
            self.utterances.addUtterance(newUtter)
        # debug prints!!!
   #     self.utterances.printAllWordsFreq()
        if self.utterances.stopwords != '':
            self.utterances.pickleFile += '_' + self.utterances.stopwords[:-4]
        if self.utterances.stem == True:
            self.utterances.pickleFile += '_stemmed'
        self.utterances.pickleFile += '.pickle'

        return None

