import bisect

class Vocabulary(object):
    def __init__(self):
        self.vocab = {}
        self.wordList = []
        self.totalWords = 0
        print('Made a blank vocabulary!') #TODO REMOVE

    def __iter__(self):
        return self.wordList.__iter__()

    def add(self, word):
        if word not in self.vocab:
            self.vocab[word] = 0
            bisect.insort(self.wordList, word)
        self.vocab[word] += 1
        self.totalWords += 1

    def getWordCount(self, word):
        return self.vocab[word]

    def getNumTotalWords(self):
        return self.totalWords

    def getNumDifferentWords(self):
        return len(self.wordList)

    def getWordList(self):
        return self.wordList

