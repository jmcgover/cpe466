#!/usr/bin/python

# CPE 466 Fall 2015
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

from __future__ import print_function

import os
import sys
import json
import pickle

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
   argParser.add_argument('-f','--file',
         action='store',
         metavar='file',
         help='the file to be parsed, appended with .json for JSON and .???? for the ???',
         required=True)
   argParser.add_argument('-s', '--stem',
         action='store_true',
         help='stems the text of the file to be parsed')
   argParser.add_argument('-sf','--stopwordfile',
         action='store',
         metavar='stopwordfile',
         help='the .txt file containing stopwords to be removed from processing')
   argParser.add_argument('-q','--queryfile',
         action='store',
         metavar='queryfile',
         help='the .txt file containing the query')
   return argParser

def argError(msg):
   if msg:
      print("%s: error: %s" % (os.path.basename(__file__), msg) )
      sys.exit(22)

def main():
   argParser = buildArguments()
   args = argParser.parse_args()
   filename = args.file
   queryfile = args.queryfile
   stopwords = args.stopwordfile

   if args.stem:
       stem = True
   else:
       stem = False
   print("----------")

   if stopwords != '' and stopwords is not None:
      if stopwords[-4:] != '.txt':
         print('Wrong stopword file format')
         return 22
   else:
      stopwords = ''

   if filename[-5:] == '.json':
      utterances = UtteranceCollection()
      try:
         with open(args.file) as raw_data_file:
            print('Processing JSON Utterances file: %s' % (args.file))
     #       data = json.load(raw_data_file)
            parser = utterance.Parser(raw_data_file, stem, stopwords, utterances)
            parser.parseUtterance()
     #       for item in data:
     #          print("PersonType: %s \t Text: %s" % (item["PersonType"], item["text"]))
     #          print(item["text"])
            print('Done!')
            print('Generating weights...')
            parser.utterances.generateWeights()
            print('Done!')
            print("----------")
      except FileNotFoundError as e:
         print('Could not find file %s' % (args.file))
         return e.errno

      try:
         with open(parser.utterances.pickleFile, "wb") as outFile:
            print("Saving to file %s" % (parser.utterances.pickleFile))
            pickle.dump(parser.utterances, outFile)
            print("Save Successful!")
            print("----------")
      except FileNotFoundError as e:
         return e.errno

      return 0
   elif filename[-7:] == '.pickle' and queryfile is not None:
      print("Opening processed file %s" % (args.file))
      try:
         with open(args.file) as pickleFile:
            utteranceCollection = pickle.load(pickleFile)
            print("Load Successful!")
       #     print(utteranceCollection.count)
            print("----------")
       #     print(utteranceCollection.printAllWordsFreq())
       #     print(utteranceCollection.vocab.getWordList())
       #     utteranceCollection.printAllWeightVectors()
      except:
         print("Something went very wrong")
         return 22
      if queryfile[-4:] == '.txt':
         print("Opening query file %s" % (args.queryfile))
     #    try:
         if True:
            with open(args.queryfile) as qfile:
               parser = query.QueryParser(qfile, utteranceCollection)
               parser.parseQuery()
     #    except FileNotFoundError as e:
     #       print('Could not find file %s' % (args.queryfile))
     #       return e.errno
      return 0
   else:
      print('File issue, make sure you include a queryfile with the .pickle results')
      return 22

if __name__ == '__main__':
    main()
