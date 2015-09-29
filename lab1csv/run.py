#!/usr/bin/python

# CPE 466 Fall 2015
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

from __future__ import print_function

import os
import sys

# Custom Libraries
sys.path.append(os.getcwd())
import argparse

import document
from document import Document

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
    argParser.add_argument('-q', '--quiet',
            action='store_true',
            help='quiet some of the output')

    # CSV Parsing Args
    argParser.add_argument('-L', '--length',
            metavar='row',
            help='computes the length of the vector at row row')
    argParser.add_argument('-D', '--dot',
            metavar='row',
            nargs=2,
            help='computes the dot product between the vectors at indices row (row can be two different values)')
    argParser.add_argument('-E', '--euclidean',
            metavar='row',
            nargs=2,
            help='computes the Euclidean Distance between the vectors at indices row (row can be two different values)')
    argParser.add_argument('-M', '--manhattan',
            metavar='row',
            nargs=2,
            help='computes the Manhattan Distance between the vectors at indices row (row can be two different values)')
    argParser.add_argument('-P', '--pearson',
            metavar='row',
            nargs=2,
            help='computes the Pearson Correlation between the vectors at indices row (row can be two different values)')

    argParser.add_argument('--min-row',
            metavar='row',
            help='computes the min value of the elements in row')
    argParser.add_argument('--max-row',
            metavar='row',
            help='computes the max value of the elements in row')
    argParser.add_argument('--median-row',
            metavar='row',
            help='computes the median value of the elements in row')
    argParser.add_argument('--mean-row',
            metavar='row',
            help='computes the mean value of the elements in row')

    argParser.add_argument('--min-col',
            metavar='column',
            help='computes the min value of the elements in column')
    argParser.add_argument('--max-col',
            metavar='column',
            help='computes the max value of the elements in column')
    argParser.add_argument('--median-col',
            metavar='column',
            help='computes the median value of the elements in column')
    argParser.add_argument('--mean-col',
            metavar='column',
            help='computes the mean value of the elements in column')

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
    print("------------")
    if filename[-3:] == 'csv':
        print('okay csv')
        csv = Custom_CSV()
        print('Opening csv...')
        try :
            with open(args.file) as file:
                print('Parsing csv...')
                parser = custom_csv.CSV_Parser(file, csv)
                parser.parseCSV()
                print('Done!')
                print("------------")
        except FileNotFoundError as e:
            print('Could not find file %s' % (args.file))
            return e.errno
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
            v = csv.getVector(row)
            if not args.quiet:
                print("row %2d: " % row, end="")
                for e in v:
                    print("%f\t" % e, end="")
                print()
            print("length: %f" % vector_math.length(v))
            print("------------")
        if args.dot:
            row1 = int(args.dot[0])
            row2 = int(args.dot[1])
            if row1 < 0 or row2 < 0:
                print('Please do not give the program negative numbers')
                return 22
            if row1 > csv.getNumVectors() or row2 > csv.getNumVectors():
                print('Row %s is out of range' % args.dot)
                return 22
            x = csv.getVector(row1)
            y = csv.getVector(row2)
            print('Computing dot product of row %d and %d...' % (row1, row2))
            if len(x) == len(y):
                if not args.quiet:
                    print("row1 %2d: " % row1, end="")
                    for e in x:
                        print("%f\t" % e, end="")
                    print()
                    print("row2 %2d: " % row2, end="")
                    for e in y:
                        print("%f\t" % e, end="")
                    print()
                print("Dot Product: %f" % vector_math.dot(x, y))
            else:
                print('Row %d does not have the same length as %d' % (row1, row2))
            print("------------")
        if args.euclidean:
            row1 = int(args.euclidean[0])
            row2 = int(args.euclidean[1])
            if row1 < 0 or row2 < 0:
                print('Please do not give the program negative numbers')
                return 22
            if row1 > csv.getNumVectors() or row2 > csv.getNumVectors():
                print('Row %s is out of range' % args.dot)
                return 22
            x = csv.getVector(row1)
            y = csv.getVector(row2)
            print('Computing Euclidean Distance of row %d and %d...' % (row1, row2))
            if len(x) == len(y):
                if not args.quiet:
                    print("row1 %2d: " % row1, end="")
                    for e in x:
                        print("%f\t" % e, end="")
                    print()
                    print("row2 %2d: " % row2, end="")
                    for e in y:
                        print("%f\t" % e, end="")
                    print()
                print("Euclidean Distance: %f" % vector_math.euclideanDistance(x, y))
            else:
                print('Row %d does not have the same length as %d' % (row1, row2))
            print("------------")
        if args.manhattan:
            row1 = int(args.manhattan[0])
            row2 = int(args.manhattan[1])
            if row1 < 0 or row2 < 0:
                print('Please do not give the program negative numbers')
                return 22
            if row1 > csv.getNumVectors() or row2 > csv.getNumVectors():
                print('Row %s is out of range' % args.dot)
                return 22
            x = csv.getVector(row1)
            y = csv.getVector(row2)
            print('Computing Manhattan Distance of row %d and %d...' % (row1, row2))
            if len(x) == len(y):
                if not args.quiet:
                    print("row1 %2d: " % row1, end="")
                    for e in x:
                        print("%f\t" % e, end="")
                    print()
                    print("row2 %2d: " % row2, end="")
                    for e in y:
                        print("%f\t" % e, end="")
                    print()
                print("Manhattan Distance  : %f" % vector_math.manhattanDistance(x, y))
            else:
                print('Row %d does not have the same length as %d' % (row1, row2))
            print("------------")
        if args.pearson:
            row1 = int(args.pearson[0])
            row2 = int(args.pearson[1])
            if row1 < 0 or row2 < 0:
                print('Please do not give the program negative numbers')
                return 22
            if row1 > csv.getNumVectors() or row2 > csv.getNumVectors():
                print('Row %s is out of range' % args.dot)
                return 22
            x = csv.getVector(row1)
            y = csv.getVector(row2)
            print('Computing Pearson Correlation of row %d and %d...' % (row1, row2))
            if len(x) == len(y):
                if not args.quiet:
                    print("row1 %2d: " % row1, end="")
                    for e in x:
                        print("%f\t" % e, end="")
                    print()
                    print("row2 %2d: " % row2, end="")
                    for e in y:
                        print("%f\t" % e, end="")
                    print()
                print("Pearson Correlation: %f" % vector_math.pearsonCorrelation(x, y))
            else:
                print('Row %d does not have the same length as %d' % (row1, row2))
            print("------------")
        if args.min_row:
            row = int(args.min_row)
            print('Computing min for row %d' % row)
            if row < 0:
                print('Please do not give the program negative numbers')
                return 22
            if row > csv.getNumVectors():
                print('Row %d is out of range' % row)
                return 22
            print('Computing min of row %d...' % row)
            v = csv.getVector(row)
            if not args.quiet:
                print("row %2d: " % row, end="")
                for e in v:
                    print("%f\t" % e, end="")
                print()
            print("min: %f" % vector_math.minRow(v))
            print("------------")
        if args.max_row:
            row = int(args.max_row)
            print('Computing max for row %d' % row)
            if row < 0:
                print('Please do not give the program negative numbers')
                return 22
            if row > csv.getNumVectors():
                print('Row %d is out of range' % row)
                return 22
            print('Computing max of row %d...' % row)
            v = csv.getVector(row)
            if not args.quiet:
                print("row %2d: " % row, end="")
                for e in v:
                    print("%f\t" % e, end="")
                print()
            print("max: %f" % vector_math.maxRow(v))
            print("------------")
        if args.median_row:
            row = int(args.median_row)
            print('Computing median for row %d' % row)
            if row < 0:
                print('Please do not give the program negative numbers')
                return 22
            if row > csv.getNumVectors():
                print('Row %d is out of range' % row)
                return 22
            print('Computing median of row %d...' % row)
            v = csv.getVector(row)
            if not args.quiet:
                print("row %2d: " % row, end="")
                for e in v:
                    print("%f\t" % e, end="")
                print()
            print("median: %f" % vector_math.medianRow(v))
            print("------------")
        if args.mean_row:
            row = int(args.mean_row)
            print('Computing mean for row %d' % row)
            if row < 0:
                print('Please do not give the program negative numbers')
                return 22
            if row > csv.getNumVectors():
                print('Row %d is out of range' % row)
                return 22
            print('Computing mean of row %d...' % row)
            v = csv.getVector(row)
            if not args.quiet:
                print("row %2d: " % row, end="")
                for e in v:
                    print("%f\t" % e, end="")
                print()
            print("mean: %f" % vector_math.meanRow(v))
            print("------------")

        if args.min_col:
            col = int(args.min_col)
            print('Computing min for col %d' % col)
            if col < 0:
                print('Please do not give the program negative numbers')
                return 22
            print('Computing min of column %d...' % col)
            c = csv.getColumn(col)
            if len(c) > 0:
                if not args.quiet:
                    print("%d" % col);
                    print("---");
                    for e in c:
                        print("%f" % e)
                print("min: %f" % vector_math.minRow(c))
            else:
                print("Column %d had no entries" % col)
            print("------------")
        if args.max_col:
            col = int(args.max_col)
            print('Computing max for col %d' % col)
            if col < 0:
                print('Please do not give the program negative numbers')
                return 22
            print('Computing max of column %d...' % col)
            c = csv.getColumn(col)
            if len(c) > 0:
                if not args.quiet:
                    print("%d" % col);
                    print("---");
                    for e in c:
                        print("%f" % e)
                print("max: %f" % vector_math.maxRow(c))
            else:
                print("Column %d had no entries" % col)
            print("------------")
        if args.median_col:
            col = int(args.median_col)
            print('Computing median for col %d' % col)
            if col < 0:
                print('Please do not give the program negative numbers')
                return 22
            print('Computing median of column %d...' % col)
            c = csv.getColumn(col)
            if len(c) > 0:
                if not args.quiet:
                    print("%d" % col);
                    print("---");
                    for e in c:
                        print("%f" % e)
                print("median: %f" % vector_math.medianRow(c))
            else:
                print("Column %d had no entries" % col)
            print("------------")
        if args.mean_col:
            col = int(args.mean_col)
            print('Computing mean for col %d' % col)
            if col < 0:
                print('Please do not give the program negative numbers')
                return 22
            print('Computing mean of column %d...' % col)
            c = csv.getColumn(col)
            if len(c) > 0:
                if not args.quiet:
                    print("%d" % col);
                    print("---");
                    for e in c:
                        print("%f" % e)
                print("mean: %f" % vector_math.meanRow(c))
            else:
                print("Column %d had no entries" % col)
            print("------------")

    elif filename[-3:] == 'txt':
        doc = Document()
        # Read Document
        print('Opening document...')
        try:
            with open(args.file) as file:
                print('Parsing document...')
                parser = document.Parser(file, doc)
                parser.parseDocument()
                print('Done!')
                print("------------")
        except FileNotFoundError as e:
            print('Could not find file %s' % (args.file))
            return e.errno
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
