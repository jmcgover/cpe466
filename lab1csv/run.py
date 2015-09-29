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

import vector_math

DESCRIPTION="CPE 466 Lab 1: A csv and text document parser."
DEF_FREQ_PERCENT = 10
DEF_TOP_WORDS = 10

def buildArguments():
    argParser = argparse.ArgumentParser(prog=sys.argv[0], description=DESCRIPTION)
    argParser.add_argument('-f', '--file',
            action='store',
            metavar='file',
            help='the file to be parsed appended with .csv for CSV and .txt for a text document',
            required=True)
    argParser.add_argument('-d', '--display-all',
            action='store_true',
            help='display either all vectors in the CSV or all words in the document')
    argParser.add_argument('-t', '--top',
            nargs='?',
            const=DEF_TOP_WORDS,
            metavar='num',
            help='displays the top num CSV rows or top num words (default is %d)' % DEF_TOP_WORDS)
    # CSV Parsing Args
    argParser.add_argument('-L', '--length',
            metavar='row',
            help='computes the length of the vector at row row')
    argParser.add_argument('-D', '--dot',
            metavar='row1 row2',
            nargs=2,
            help='computes the dot product between the vectors at row1 and row2')

    # Document Parsing Args
    argParser.add_argument('-m', '--most-frequent',
            action='store_true',
            help='displays the most frequent word')
    argParser.add_argument('-p', '--most-frequent-percent',
            nargs='?',
            const=DEF_FREQ_PERCENT,
            metavar='percent',
            help='displays the words within percent percent frequency \
                    of the most frequent word [0,100] (default is %d percent)' % DEF_FREQ_PERCENT)
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
    argParser = buildArguments()
    args = argParser.parse_args()
    filename = args.file
    print(args)
    print("------------")
    if filename[-3:] == 'csv':
        print('okay csv')
        csv = Custom_CSV()
        print('Opening csv...')
        with open(args.file) as file:
            print('Parsing csv...')
            parser = custom_csv.CSV_Parser(file, csv)
            parser.parseCSV()
            print('Done!')
            print("------------")
        if args.display_all:
            print('Displaying all vectors and their rows...')
            print('%-16s %-13s' % ('Row', 'Vector'))
            for i in range(0,csv.getNumVectors()):
                print("%d: " % i, end="")
                for e in csv.getVector(i):
                    print("%f\t" % e, end="")
                print()
            print("------------")
        if args.top:
            top = int(args.top)
            if top < 0:
                print('Please do not give the program negative numbers')
                return 22
            if top > csv.getNumVectors():
                print('Row %d is out of range' % top)
                return 22
            print('Displaying top %d rows...' % top)
            print('%-16s %-13s' % ('Row', 'Vector'))
            for i in range(0,top):
                print("%d: " % i, end="")
                for e in csv.getVector(i):
                    print("%f\t" % e, end="")
                print()
            print("------------")
        if args.length:
            row = int(args.length)
            if row < 0:
                print('Please do not give the program negative numbers')
                return 22
            if row > csv.getNumVectors():
                print('Row %d is out of range' % row)
                return 22
            print('Computing length of row %d...' % row)
            print("row %2d: " % row, end="")
            v = csv.getVector(row)
            for e in v:
                print("%f\t" % e, end="")
            print()
            print("length: %f" % vector_math.length(v))
            print("------------")
    elif filename[-3:] == 'txt':
        doc = Document()
        # Read Document
        print('Opening document...')
        with open(args.file) as file:
            print('Parsing document...')
            parser = document.Parser(file, doc)
            parser.parseDocument()
            print('Done!')
            print("------------")
        # Display Document
        if args.display_all:
            print('Displaying all words and their occurrences...')
            print('%-16s %-13s' % ('Word', 'Occurrences'))
            for w in doc:
                print('%-16s %-13d' % (w, doc.getWordCount(w)))
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
        if args.top:
            topNum = int(args.top)
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

    else:
        print('Please provide either a .csv or a .txt file to be parsed')
        return 22
    return 0

if __name__ == '__main__':
    main()
