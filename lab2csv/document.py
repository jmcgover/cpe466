#! /usr/bin/python

# CPE 466 Fall 2015
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

from __future__ import print_function

import os
import re
import sys

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
    def getNMostCommonWords(self, n):
        sortedVocab = sorted(self.vocab.items(), key=operator.itemgetter(1))
        sortedByFreqWords = []
        for w in reversed(sortedVocab):
            sortedByFreqWords.append(w[0])
        return sortedByFreqWords[:n]
    def getWordsAboveFrequency(self, freq):
        wordsAbove = []
        for w in self.vocab:
            if self.getWordCount(w) > freq:
                wordsAbove.append(w)
        return wordsAbove
    def getWordsEqualToFrequency(self, freq):
        wordsEqual = []
        for w in self.vocab:
            if self.getWordCount(w) == freq:
                wordsEqual.append(w)
        return wordsEqual


# DOCUMENT
class Document(object):
    def __init__(self):
        self.vocab = Vocabulary()
        self.paragraphs = 0
        self.sentences = 0
        self.countedParagraph = False
#        print('Made a new document class!') #TODO REMOVE
    def __iter__(self):
        return self.vocab.__iter__()

    def addWord(self, word):
        self.vocab.add(word)

    def addSentence(self, num=1):
        self.sentences += num

    def addParagraph(self, num=1):
        self.paragraphs += num

    def getWordCount(self, word):
        return self.vocab.getWordCount(word)

    def getNumTotalWords(self):
        return self.vocab.getNumTotalWords()

    def getNumDifferentWords(self):
        return self.vocab.getNumDifferentWords()

    def getNumSentences(self):
        return self.sentences

    def getNumParagraphs(self):
        return self.paragraphs

    def getMostFrequentWord(self):
        mostFrequentCount = 0
        mostFrequentWord = None
        for w in self.vocab:
            if self.getWordCount(w) > mostFrequentCount:
                mostFrequentWord = w
                mostFrequentCount = self.getWordCount(w)
        return mostFrequentWord
    def getMostFrequentWords(self, percent):
        mostFrequentWord = self.getMostFrequentWord()
        mostFrequentCount = self.getWordCount(mostFrequentWord)
        lowerBound = mostFrequentCount - (mostFrequentCount * percent / 100)
        mostFrequentWords = []
        for w in self.vocab:
            if self.getWordCount(w) >= lowerBound:
                mostFrequentWords.append(w)
        return mostFrequentWords
    def getTopWords(self, topNum):
        return self.vocab.getNMostCommonWords(topNum)
    def getWordsAboveFrequency(self, freq):
        return self.vocab.getWordsAboveFrequency(freq)
    def getWordsEqualToFrequency(self, freq):
        return self.vocab.getWordsEqualToFrequency(freq)


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
    def __init__(self, file, document):
        self.file = file
        self.document = document
        self.vocab = Vocabulary()
        self.numLines = 0
#        print('Building a parser!') #TODO REMOVE

    def parseDocument(self):
        for line in self.file:
            self.numLines += 1
            if line == "\n":
                if not self.countedParagraph:
                    self.document.addParagraph()
                    self.countedParagraph = True
            else:
                self.countedParagraph = False
                line = line.strip()
                punctMarks = regexSent.findall(line)
                self.document.addSentence(num=len(punctMarks))
                sentences = regexSent.split(line)
                sentences = filter(None, sentences)
                for s in sentences:
                    s = s.strip()
                    words = regexWord.split(s)
                    words = filter(None, words)
                    for w in words:
                        w = w.strip("'").strip('-')
                        if w:
                            self.document.addWord(w)
        return None

