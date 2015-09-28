#! /usr/bin/python

import os
import re
import sys

# Custom files
sys.path.append(os.getcwd())
from vocabulary import Vocabulary

# SENTENCE
#class Sentence(object):
#    def __init__(self):
#        self.vocab = Vocabulary()
#        print('Started a new sentence!') #TODO REMOVE
#
#    def addWords(self, words):
#        for w in words:
#            self.vocab.addWord(w)
## PARAGRAPH
#class Paragraph(object):
#    def __init__(self):
#        self.vocab = Vocabulary()
#        self.sentences = []
#        print('Found a new paragraph!') #TODO REMOVE
#
#    def addWords(self, words):
#        for w in words:
#            self.vocab.addWord(w)
#    def addSentences(self, sentences):
#        for s in sentences:
#            self.sentences.append(sentence)

# DOCUMENT
class Document(object):
    def __init__(self):
        self.vocab = Vocabulary()
        self.paragraphs = 0
        self.sentences = 0
        print('Made a new document class!') #TODO REMOVE
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
        print('Building a parser!') #TODO REMOVE

    def parseDocument(self):
        for line in self.file:
            self.numLines += 1
            if line == "\n":
                self.document.addParagraph()
            else:
                line = line.strip()
                punctMarks = regexSent.findall(line)
                self.document.addSentence(num=len(punctMarks))
                sentences = regexSent.split(line)
                sentences = filter(None, sentences)
                print("%d: %s" % (self.numLines, line))
                for s in sentences:
                    s = s.strip()
                    print("\t[%s]" % (s))
                    print("\t\t", end="")
                    words = regexWord.split(s)
                    words = filter(None, words)
                    for w in words:
                        w = w.strip("'")
                        if w:
                            self.document.addWord(w)
                            print("{%s}" % (w), end="")
                    print()
                print()
        print("Sent: %s" % DELIM_SENT)
        print("Word: %s" % DELIM_WORD)
        return None

