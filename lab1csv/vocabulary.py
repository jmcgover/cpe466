#! /usr/bin/python

# CPE 466 Fall 2015
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

from __future__ import print_function
import bisect

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

