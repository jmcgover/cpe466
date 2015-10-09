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
        commonTerms[word] = 1
    for term in q:
        commonTerms[word] = 1
    dotProduct = 0.0
    for term in commonTerms:
        dotProduct += d.getTermWeight(term) * q.getTermWeight(term)
    return dotProduct / (d.getNorm() * q.getNorm())

# QUERY Result
class QueryResult(object):
    def __init__(self, d, q):
        self.document = d
        self.query = q
        self.similarity = cosine_similarity(self.document, self.query)
    def __lt__(self, other):
        return self.similarity < other.similarity
    def __gt__(self, other):
        return self.similarity > other.similarity
    def __le__(self, other):
        return self.similarity <= other.similarity
    def __ge__(self, other):
        return self.similarity >= other.similarity
    def getDocument(self):
        return self.document
    def getQuery(self):
        return self.query

# QUERY
class Query(object):
    def __init__(self, text, collection, stemmer=None, stopwords=None):
        self.text = text
        self.collection = collection
        self.results = {}
        self.vocab = Vocabulary()
        self.maxFreq = 0

        self.norm = None
        self.weights = None

        # Parse
        parser = UtteranceTextParser(stemmer, stopwords)
        for line in text:
            for word in parser.getWords(line):
                self.vocabulary.add(word)
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

    def calculateNorm(self):
        sumSquares = 0.0
        for weight in self.getWeights():
            sumSquares += weight * weight
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
    def findResults(self):
        self.results = []
        for doc in self.collections.getDocuments():
            sim = cosineSimilarity(doc, query)
    def getResults(self):
        if not results:
            self.findResults()
        return self.results


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

