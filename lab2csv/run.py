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

# Custom Libraries
sys.path.append(os.getcwd())
import argparse
import utterance
from utterance import UtteranceCollection
import query
from query import Query

DESCRIPTION="CPE 466 Lab 2: Information Retrieval from Digital Democracy."

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
    argParser.add_argument('-w','--stopword-file',
            action='store',
            metavar='stopwordfile',
            help='the .txt file containing stopwords to be removed from processing')
    argParser.add_argument('-q','--query-filename',
            action='store',
            metavar='query-filename',
            help='the .txt file containing the query')
    return argParser

def argError(msg):
    if msg:
        print("%s: error: %s" % (os.path.basename(__file__), msg) )
        sys.exit(22)

def main():
    argParser = buildArguments()
    args = argParser.parse_args()
    stopwords = args.stopword_file

    if args.stem:
        stem = True
    else:
        stem = False
    print("----------")

    if stopwords != '' and stopwords is not None:
        if stopwords[-4:] != '.txt':
            print('Wrong stopword file format')
            return errno.EINVAL
    else:
        stopwords = ''

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
        collection = UtteranceCollection(jsonData)
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
    if args.query_filename and args.query_filename[-4:] == '.txt':
        queryText = None
        print("Opening query file %s" % (args.query_filename))
        try:
            with open(args.query_filename) as qfile:
                queryText = qfile.readlines()
        except OSError as e:
            if e.errno == errno.ENOENT:
                print('Could not find file %s' % (args.filename))
                return errno.ENOENT
            else:
                raise
        query = Query(queryText, collection)
        print("Finding documents related to:")
        print("%s" % queryText)
        query.findResults()
        for res in query.getResults(5):
            print("%.3f:%d: %s" % (res.getSimilarity(), res.getDocument().pid, res.getDocument().text))

if __name__ == '__main__':
    rtn = main()
    exit(rtn)
