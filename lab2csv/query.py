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
from utterance import UtteranceTextParser
import bisect
import operator

def cosineSimilarity(d, q):
    commonTerms = {}
    for term in d:
        commonTerms[term] = 1
    for term in q:
        commonTerms[term] = 1
    dotProduct = 0.0
    for term in commonTerms:
        dotProduct += d.getTermWeight(term) * q.getTermWeight(term)
    return dotProduct / (d.getNorm() * q.getNorm())

# QUERY Result
class QueryResult(object):
    def __init__(self, d, q):
        self.document = d
        self.query = q
        self.similarity = cosineSimilarity(self.document, self.query)
    def __lt__(self, other):
        return self.similarity > other.similarity
    def __gt__(self, other):
        return self.similarity < other.similarity
    def __le__(self, other):
        return self.similarity >= other.similarity
    def __ge__(self, other):
        return self.similarity <= other.similarity
    def __cmp__(self, other):
        return -1 * (self.similarity - other.similarity)
    def getDocument(self):
        return self.document
    def getQuery(self):
        return self.query
    def getSimilarity(self):
        return self.similarity

# QUERY
class Query(object):
    def __init__(self, text, collection, stemmer=None, stopwordVocab=None):
        self.text = text
        self.collection = collection
        self.results = {}
        self.vocab = Vocabulary()
        self.maxFreq = 0

        self.norm = None
        self.weights = None

        # Parse
        self.parser = UtteranceTextParser(stemmer, stopwordVocab)
        for word in self.parser.getWords(text):
            self.vocab.add(word)
        for word in self.getWordList():
            if self.getWordCount(word) > self.maxFreq:
                self.maxFreq = self.getWordCount(word)

    def __iter__(self):
        return self.vocab.__iter__()

    def addWord(self, word):
        self.vocab.add(word)

    def getWordCount(self, word):
        return self.vocab.getWordCount(word)

    def getWordList(self):
        return self.vocab.getWordList()

    # Term Weights
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
            tf = self.getWordCount(term)
            idf = self.collection.inverseDocumentFrequency(term)
            self.weights[term] = tf * idf
    def getWeights(self):
        if not self.weights:
            self.calculateWeights()
        return self.weights
    def getTermWeight(self, term):
        weights = self.getWeights()
        if term not in weights:
            return 0
        return weights[term]
    def printStatistics(self, string):
        for w in self.parser.getWords(string):
            print("Query Stats")
            print("Word: %s"   % w)
            print("TF  : %d"   % self.getWordCount(w))
            print("IDF : %.3f" % self.collection.inverseDocumentFrequency(w))
            print("WGHT: %.3f" % self.getTermWeight(w))

    # Results
    def findResults(self):
        self.results = []
        for doc in self.collection.getDocuments():
            result = QueryResult(doc, self)
            bisect.insort(self.results, result)
    def getResults(self, topK=None):
        if not self.results:
            self.findResults()
        if topK:
            return self.results[:topK]
        return self.results
