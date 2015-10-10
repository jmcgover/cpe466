#!/usr/bin/python

# CPE 466 Fall 2015
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

from __future__ import print_function

import errno
import json
import os
import pickle
import sys
import textwrap

# Custom Libraries
sys.path.append(os.getcwd())
import argparse
import utterance

from utterance import UtteranceCollection
from utterance import Vocabulary
from stemming import PorterStemmer

import query
from query import Query

WIDTH=100
INDENT=4
DESCRIPTION="CPE 466 Lab 2: Information Retrieval from Digital Democracy."
DEF_TOP = 10
def buildArguments():
    argParser = argparse.ArgumentParser(prog=sys.argv[0], description=DESCRIPTION)
    argParser.add_argument('-f','--filename',
            action='store',
            metavar='filename',
            help='the file to be parsed, appended with .json for JSON',
            required=True)
    argParser.add_argument('-s', '--stem',
            action='store_true',
            help='stems the text of the file to be parsed')
    argParser.add_argument('-w','--stopword-filename',
            action='store',
            metavar='filename',
            help='the .txt file containing stopwords to be removed from processing')
    argParser.add_argument('-q','--query-filename',
            action='store',
            metavar='filename',
            help='the .txt file containing the query')
    argParser.add_argument('-t', '--top',
            nargs='?',
            const=DEF_TOP,
            metavar='num',
            help='displays the top num results (default is %d)' % DEF_TOP)
    argParser.add_argument('-d', '--dedup',
            action='store_true',
            help='deduplicates utterances based off of pid, first last name, date, and text')
    argParser.add_argument('-m', '--metadata',
            action='store_true',
            help='treats metadata as included text')
    argParser.add_argument('-W','--word',
            action='store',
            metavar='word1,word2,...',
            help='comma-separated list of words ')
    return argParser

def argError(msg):
    if msg:
        print("%s: error: %s" % (os.path.basename(__file__), msg) )
        sys.exit(22)

def main():
    # ARGUMENT PARSING
    argParser = buildArguments()
    args = argParser.parse_args()

    print("----------")
    # STEMMING CREATION
    stemmer = None
    if args.stem:
        stemmer = PorterStemmer()

    # STOPWORD CREATION
    stopwordVocab = None
    if args.stopword_filename:
        stopwordList = None
        if args.stopword_filename[-4:] != '.txt':
            print('Wrong stopword file format: please provide a .txt file')
            return errno.EINVAL
        try:
            with open(args.filename) as raw_data_file:
                print('Building stopword vocabulary: %s' % (args.stopword_filename))
                stopwordList = raw_data_file.readlines()
        except OSError as e:
            if e.errno == errno.ENOENT:
                print('Could not find stopword file %s' % (args.file))
                return errno.ENOENT
        stopwordVocab = Vocabulary()
        for w in stopwordList:
            stopwordVocab.add(w)

    # COLLECTION CREATION
    collection = None
    if args.filename[-5:] == '.json':
        try:
            with open(args.filename) as raw_data_file:
                print('Processing JSON Utterances file: %s' % (args.filename))
                jsonData = None
                try:
                    jsonData = json.load(raw_data_file)
                except ValueError as err:
                    print("failed to open JSON file")
                    return errno.EINVAL
        except OSError as e:
            if e.errno == errno.ENOENT:
                print('Could not find file %s' % (args.file))
                return errno.ENOENT
        collection = UtteranceCollection(jsonData, stemmer=stemmer, stopwordVocab=stopwordVocab, dedup=args.dedup, metadata=args.metadata)
        print('Done!')
        print("----------")
#        if args.pickle:
#            try:
#                pickleFilename = args.filename.replace(".","_") + ".pickle"
#                print("Saving to file %s" % (pickleFilename))
#                with open(pickleFilename, "wb") as outFile:
#                    pickle.dump(collection, outFile)
#                    print("Save Successful!")
#                    print("----------")
#            except OSError as e:
#                if e.errno == errno.ENOENT:
#                    print('Could not open file %s' % (args.filename))
#                    return errno.ENOENT
    elif args.filename[-7:] == '.pickle' and queryfile is not None:
        print("Opening processed file %s" % (args.file))
        try:
            with open(args.file) as pickleFile:
                collection = pickle.load(pickleFile)
                print("Load Successful!")
                print("----------")
        except:
            print("Something went very wrong")
            return 22
    else:
        print('File issue, make sure you include a queryfile with the .pickle results')
        return errno.EINVAL
    # QUERYING
    if args.query_filename and args.query_filename[-4:] == '.txt':
        # TOP RESULTS
        topResultNum = int(args.top) if args.top else DEF_TOP
        queryText = None
        # OPEN QUERY FILE
        print("Opening query file: %s" % (args.query_filename))
        try:
            with open(args.query_filename) as qfile:
                queryText = qfile.read().replace("\n", " ").strip()
        except OSError as e:
            if e.errno == errno.ENOENT:
                print('Could not find file %s' % (args.filename))
                return errno.ENOENT
            else:
                raise
        query = Query(queryText, collection, stemmer=stemmer, stopwordVocab=stopwordVocab)
        print("Finding documents related to:")
        print('~' * WIDTH)
        dedented_text = textwrap.dedent(queryText).strip()
        print(textwrap.fill(dedented_text, initial_indent='    ', subsequent_indent='    ', width = 100))
        query.findResults()
        print('~' * WIDTH)
        print("Finding top %s results" % topResultNum)
        print('~' * WIDTH)
        i = 1
        for res in query.getResults(topResultNum):
            doc = res.getDocument()
            resultStr = "%-2d|%.3f\tpid:%d\tperson:%s" % \
                (i, res.getSimilarity(), doc.pid, doc.PersonType)
            print(resultStr)
            print('~' * WIDTH)
            dedented_text = textwrap.dedent(doc.text).strip()
            print(textwrap.fill(dedented_text, initial_indent=' ' * INDENT, subsequent_indent=' ' * INDENT, width = WIDTH))
            print('~' * WIDTH)
            i += 1
    if args.word:
        print("----------")
        collection.printStatistics(args.word)
        print("----------")
        query.printStatistics(args.word)
        print("----------")
if __name__ == '__main__':
    rtn = main()
    exit(rtn)
