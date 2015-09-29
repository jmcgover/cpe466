#!/usr/bin/python
from __future__ import print_function

import argparse
import os
import sys

# Custom Libraries
sys.path.append(os.getcwd())
import document
from document import Document
from vocabulary import Vocabulary

import custom_csv
from custom_csv import Custom_CSV

DESCRIPTION="CPE 466 Lab 1: A csv and text document parser."
DEF_FREQ_PERCENT = 10
DEF_TOP_WORDS = 10

def buildArguments():
    argParser = argparse.ArgumentParser(description=DESCRIPTION)
    argParser.add_argument('-f', '--file',
            action='store',
            metavar='file',
            help='the file to be parsed appended with .csv for CSV and .txt for a text document',
            required=True)
    argParser.add_argument('-m', '--most-frequent',
            action='store_true',
            help='displays the most frequent word')
    argParser.add_argument('-p', '--most-frequent-percent',
            nargs='?',
            const=DEF_FREQ_PERCENT,
            metavar='percent',
            help='displays the words within percent percent frequency \
                    of the most frequent word [0,100] (default is %d percent)' % DEF_FREQ_PERCENT)
    argParser.add_argument('-t', '--top-words',
            nargs='?',
            const=DEF_TOP_WORDS,
            metavar='num',
            help='displays the top num words (default is %d)' % DEF_TOP_WORDS)
    argParser.add_argument('-w', '--word',
            metavar='word1,word2,...',
            help='displays the frequency of the specified words')
    argParser.add_argument('-i', '--is-in',
            metavar='word',
            help='checks whether word is in the document')
    argParser.add_argument('-e', '--equal-to',
            metavar='frequency',
            help='displays all words above frequency in document')
    argParser.add_argument('-a', '--above',
            metavar='frequency',
            help='displays all words equal to frequency in document')
    argParser.add_argument('-s', '--stats',
            action='store_true',
            help='displays the number of words, different words, sentences, and paragraphs found in the document')

    return argParser

def argError(msg):
    if msg:
        print("%s: error: %s" % (os.path.basename(__file__), msg) )
    sys.exit(22)

def main():
    print("------------")
    argParser = buildArguments()
    args = argParser.parse_args()
    filename = args.file
    print(args)
    if filename[-3:] == 'txt':
        print('Opening document...')
        doc = Document()
        with open(args.file) as file:
            print('Parsing document...')
            parser = document.Parser(file, doc)
            parser.parseDocument()
            print('Done!')
            print("------------")
        if args.most_frequent:
            print('Finding most frequent...')
            mostFreq = doc.getMostFrequentWord()
            print('%-16s %-13s' % ('Most Frequent', 'Occurrences'))
            print('%-16s %-13d' % (mostFreq, doc.getWordCount(mostFreq)))
            print("------------")
        if args.most_frequent_percent:
            percent = int(args.most_frequent_percent)
            if percent > 100 or percent < 0:
                print('%d is an invalid percentage -- must be between 0 and 100' % percent)
                return 22
            print('Finding words within %d percent of the most frequent...' % percent)
            mostFreqWords = doc.getMostFrequentWords(percent)
            print('%-16s %-13s' % ('Most Frequent', 'Occurrences'))
            for w in mostFreqWords:
                print('%-16s %-13d' % (w, doc.getWordCount(w)))
            print("------------")
        if args.top_words:
            topNum = int(args.top_words)
            if topNum < 0:
                print('Please do not give the program negative numbers')
                return 22
            print('Finding top %d words...' % topNum)
            topWords = doc.getTopWords(topNum)
            print('%-16s %-13s' % ('Top %d Frequent' % topNum, 'Occurrences'))
            for w in topWords:
                print('%-16s %-13d' % (w, doc.getWordCount(w)))
            print("------------")
        if args.equal_to:
            freq = int(args.equal_to)
            print('Finding words with %d ocurrences...' % freq)
            wordsEqual = doc.getWordsEqualToFrequency(freq)
            print('%-16s %-13s' % ('Word', 'Occurrences'))
            wordsEqual = sorted(wordsEqual)
            for w in wordsEqual:
                print('%-16s %-13d' % (w, doc.getWordCount(w)))
            print("------------")
        if args.above:
            freq = int(args.above)
            print('Finding words above %d occurrences...' % freq)
            wordsAbove = doc.getWordsAboveFrequency(freq)
            print('%-16s %-13s' % ('Word', 'Occurrences'))
            wordsAbove = sorted(wordsAbove)
            for w in wordsAbove:
                print('%-16s %-13d' % (w, doc.getWordCount(w)))
            print("------------")
        if args.word:
            print('Finding occurrences for %s...' % args.word)
            print('%-16s %-13s' % ('Word', 'Occurrences'))
            for w in args.word.split(','):
                print('%-16s %-13d' % (w, doc.getWordCount(w)))
            print("------------")
        if args.is_in:
            print('Checking if %s is in the document...' % args.is_in)
            if doc.getWordCount(args.is_in) > 0:
                print('"%s" IS in the document!' % args.is_in)
            else:
                print('"%s" IS NOT in the document!' % args.is_in)
            print("------------")
        if args.stats:
            print("Document Statistics:")
            print("Number Total Words    : %d" % (doc.getNumTotalWords()))
            print("Number Different Words: %d" % (doc.getNumDifferentWords()))
            print("Number of Sentences   : %d" % (doc.getNumSentences()))
            print("Number of Paragraphs  : %d" % (doc.getNumParagraphs()))
            print("------------")

    elif filename[-3:] == 'csv':
        print('okay csv')
    else:
        print('Please provide either a .csv or a .txt file to be parsed')
        return 22
    return 0

if __name__ == '__main__':
    main()
