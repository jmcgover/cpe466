#! /usr/bin/python

# CPE 466 Fall 2015
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

from __future__ import print_function

import os
import re
import sys
import json
import math

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

class InvertedIndex(object):
    def __init__(self):
        self.index = {}
        self.wordList = []
        self.totalWords = 0

    def __iter__(self):
        return self.wordList.__iter__()

    def add(self, word):
        if word not in self.index:
            self.index[word] = 0
            bisect.insort(self.wordList, word)
        self.index[word] += 1
        self.totalWords += 1

    def getDocumentFrequency(self, word):
        if word in self.index:
            return self.index[word]
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
    def __init__(self, jsonEntry, collection):
        self.__dict__ = jsonEntry
        keys = []
        for key in jsonEntry.keys():
            keys.append(key)
        self.jsonKeys = keys
        self.collection = collection
        self.vocab = Vocabulary()

        self.norm = None
        self.weights = None

    def __iter__(self):
        return self.vocab.__iter__()

    def addWord(self, word):
        self.vocab.add(word)

    def getWordList(self):
        return self.vocab.getWordList()

    def getWordCount(self, word):
        return self.vocab.getWordCount(word)

    def getJSONKeys(self):
        return self.jsonKeys
    def setTermWeightsVector(self, vector):
        self.vector = vector

    def calculateNorm(self):
        sumSquares = 0.0
        weights = self.getWeights()
        for w in weights:
            sumSquares += weights[w] * weights[w]
        self.norm = math.sqrt(sumSquares)
    def getNorm(self):
        if not self.norm:
            self.calculateNorm()
        return self.norm
    def calculateWeights(self):
        self.weights = {}
        for term in self.getWordList():
            self.weights[term] = self.collection.tf_idf(term, self)
    def getTermWeight(self, term):
        weights = self.getWeights()
        if term not in weights:
            return 0
        return weights[term]
    def getWeights(self):
        if not self.weights:
            self.calculateWeights()
        return self.weights

# TODO finish this to handle the dupes in the JSON file
    def compareUtterances(self, other):
        if self.pid == otherUtter.pid:
           if self.text == other.text:
              return True
        return False



# UTTERANCE COLLECTION
class UtteranceCollection(object):
    def __init__(self, jsonData, stemmer=None, stopwords=None):
        self.index = InvertedIndex()
        self.vocab = Vocabulary()
        self.utterances = []
        self.numUtterances = 0
        self.maxFreq = 0

        # Parse
        parser = UtteranceTextParser(stemmer, stopwords)
        for entry in jsonData:
            utterance = Utterance(entry, self)
            for word in parser.getWords(utterance.text):
                utterance.addWord(word)
                self.vocab.add(word)
            for word in utterance.getWordList():
                self.index.add(word)
                if utterance.getWordCount(word) > self.maxFreq:
                    self.maxFreq = utterance.getWordCount(word)
            self.utterances.append(utterance)
            self.numUtterances += 1

        print("Num Total Words    : %d" % self.vocab.getNumTotalWords())
        print("Num Different Words: %d" % self.vocab.getNumDifferentWords())
        print("Calculating weights...")
        for doc in self.utterances:
            doc.calculateNorm()
            doc.calculateWeights()
#            print("%d: %f: " % (doc.pid, doc.getNorm()), end="")
#            weights = doc.getWeights()
#            for key in weights.keys():
#                print("%s:%.2f|" % (key,weights[key]), end="")
#            print()

    def __iter__(self):
        return self.vocab.__iter__()

    def addWord(self, word):
        self.vocab.add(word)

    def getDocuments(self):
        return self.utterances

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
        for w in words:
            print("%s: %d" % (w , self.vocab.getWordCount(w)))

    # Term Frequency
    def termFrequency(self, term, document):
        if self.getMaxFrequency() == 0:
            return 0
        return float(self.rawFrequency(term, document)) / self.getMaxFrequency()
        #return 0.5 + 0.5 * self.rawFrequency(term, document) / float(self.getMaxFrequency())
    def rawFrequency(self, term, document):
        return document.getWordCount(term)
    def getMaxFrequency(self):
        return self.maxFreq

    # Inverse Document Frequency
    def inverseDocumentFrequency(self, term):
        if self.index.getDocumentFrequency(term) == 0:
            return 0
        return math.log(float(self.numUtterances) / self.index.getDocumentFrequency(term))
    def tf_idf(self, term, document):
        tf = self.termFrequency(term, document)
        idf = self.inverseDocumentFrequency(term)
        return tf * idf

    def generateWeights(self):
        words = self.vocab.getWordList()
        for w in words:
            wordCount = self.getWordCount(w)
            idf = math.log((self.numUtterances/float(wordCount)),2)
            maxFreq = 0.0
            for utter in self.utterances:
                freq = utter.getWordCount(w)
                if freq > maxFreq:
                    maxFreq = float(freq)

            for utter in self.utterances:
                if utter.vector != '':
                    utter.vector += ','
                if utter.getWordCount(w) == 0:
                    utter.vector += '0'
                #    utter.vector += '' # sparse vector option
                else:
                    weight = ((utter.getWordCount(w))/maxFreq) * idf
                    utter.vector += str(weight)

    def printAllWeightVectors(self):
        for utter in self.utterances:
            print(utter.vector)

# DELIMITERS
DELIM_SENT = "\.|!|\?"

DELIM_WORD =  "\s+"                 # White Space
DELIM_WORD += "%s|%s" % ("|,|:|;|\(|\)", DELIM_SENT)        # Punctuation
# DELIM_WORD += "|,|:|;|\(|\)"        # Punctuation
DELIM_WORD += "|\s-+\s"             # Non-Hyphen Dashes
# DELIM_WORD += "|(\s+|^)'|'(\s+|$)|^'(\s+)"  # Single Quotation
DELIM_WORD += "|\""                 # Double Quotation
DELIM_WORD += "|\.{3}"              # Ellipses

def isEmpty(str):
    if str:
        str.strip()
    return not (str == "" or str == None)

class UtteranceTextParser(object):
    def __init__(self, stemmer=None, stopwords=None):
        self.regexSent = re.compile(DELIM_SENT)
        self.regexWord = re.compile(DELIM_WORD)
        self.stemmer = stemmer

    def getWords(self, text):
        textWords = []
        if text != "\n":
            text = text.strip()
            sentences = self.regexSent.split(text)
            sentences = filter(None, sentences)
            for s in sentences:
                s = s.strip()
                words = self.regexWord.split(s)
                words = filter(None, words)
                for w in words:
                    w = w.lower()
                    w = w.strip("'").strip('-')
                    if w:
                        if self.stemmer and w.isalpha():
                            w = stemmer.stem(w,0,len(w)-1)
                        textWords.append(w)
        return textWords

# PARSER
class Parser(object):
    def __init__(self, file, stem, stopwords, utterances):
        self.file = file
        self.utterances = utterances
        self.utterances.stem = stem
        self.utterances.stopwords = stopwords
        self.utterances.stopwordList = []
        self.utterances.pickleFile = "SB277_Processed"

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
                            if newUtter.getWordCount(newWord) == 1:
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

