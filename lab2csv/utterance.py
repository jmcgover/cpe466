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
    def isIn(self, word):
        return self.getWordCount(word) > 0

    def isNotIn(self, word):
        return self.getWordCount(word) == 0

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
    def __hash__(self):
        return hash((self.pid, self.last, self.first, self.date, self.text))
    def __eq__(self, other):
        return self.pid == other.pid\
                and self.last == other.last\
                and self.first == other.first\
                and self.date == other.date\
                and self.text == other.text

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
    def __init__(self, jsonData, stemmer=None, stopwordVocab=None, dedup=False, metadata=False):
        self.index = InvertedIndex()
        self.vocab = Vocabulary()
        self.utterances = {}
        self.numUtterances = 0
        self.maxFreq = 0
        if metadata: 
            print("METADATA: Incorporating metadata")
        if dedup: 
            print("DEDUP: Deduplicating documents")

        # Parse
        self.parser = UtteranceTextParser(stemmer=stemmer, stopwordVocab=stopwordVocab)
        for entry in jsonData:
            utterance = Utterance(entry, self)
            for word in self.parser.getWords(utterance.text):
                utterance.addWord(word)
                self.vocab.add(word)
            if dedup:
                # DEDUP
                if utterance not in self.utterances:
                    if metadata:
                        for key in utterance.getJSONKeys():
                            if not isinstance(utterance.__dict__[key],(int, long, float, complex)):
                                utterance.addWord(utterance.__dict__[key].lower())
                    for word in utterance.getWordList():
                        self.index.add(word)
                        if utterance.getWordCount(word) > self.maxFreq:
                            self.maxFreq = utterance.getWordCount(word)
                    self.utterances[utterance] = utterance
                    self.numUtterances += 1
                else:
                    newlyAddedVocab = Vocabulary()
                    oldUtterance = self.utterances[utterance]
                    oldKeys = oldUtterance.getJSONKeys();
                    newKeys = utterance.getJSONKeys();
                    for key in newKeys:
                        if key not in oldKeys:
                            oldUtterance[key] = utterance[key]
                    for key in oldKeys:
                        if oldUtterance.__dict__[key] != utterance.__dict__[key]\
                                and isinstance(utterance.__dict__[key],basestring)\
                                and utterance.__dict__[key].isalpha():
                            oldUtterance.__dict__[key] += "," + utterance.__dict__[key]
                            if metadata:
                                for word in self.parser.getWords(utterance.__dict__[key]):
                                    oldUtterance.addWord(word)
                                    self.vocab.add(word)
                                    newlyAddedVocab.add(word)
                    if metadata:
                        for word in newlyAddedVocab:
                            self.index.add(word)
                            if oldUtterance.getWordCount(word) > self.maxFreq:
                                self.maxFreq = oldUtterance.getWordCount(word)
            else:
                # NO DEDUP
                for word in utterance.getWordList():
                    self.index.add(word)
                    if utterance.getWordCount(word) > self.maxFreq:
                            self.maxFreq = utterance.getWordCount(word)
                    self.utterances[utterance] = utterance
                    self.numUtterances += 1
                if metadata:
                    for key in utterance.getJSONKeys():
                        if not isinstance(utterance.__dict__[key],(int, long, float, complex)):
                            for word in self.parser.getWords(utterance.__dict__[key]):
                                utterance.addWord(word)
                                self.vocab.add(word)


        print("Calculating weights...")
        for doc in self.utterances:
            doc.calculateNorm()
            doc.calculateWeights()

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

    def printAllWeightVectors(self):
        for utter in self.utterances:
            print(utter.vector)

    def printStatistics(self, string):
        for w in self.parser.getWords(string):
            print("Global Stats")
            print("Word: %s" % w)
            print("TF  : %d" % self.getWordCount(w))
            print("IDF : %.3f" % self.inverseDocumentFrequency(w))


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
    def __init__(self, stemmer=None, stopwordVocab=None):
        self.regexSent = re.compile(DELIM_SENT)
        self.regexWord = re.compile(DELIM_WORD)
        self.stemmer = stemmer
        self.stopwordVocab = stopwordVocab

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
                        if self.stopwordVocab is None or self.stopwordVocab.getWordCount(w) == 0:
                            if self.stemmer and w.isalpha():
                                w = self.stemmer.stem(w,0,len(w)-1)
                            textWords.append(w)
        return textWords
