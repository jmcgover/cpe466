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
import json

import utterance
from utterance import UtteranceCollection

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

   return argParser

def argError(msg):
   if msg:
      print("%s: error: %s" % (os.path.basename(__file__), msg) )
      sys.exit(22)

def main():
   argParser = buildArguments()
   args = argParser.parse_args()
   filename = args.file
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

   if filename[-4:] == 'json':
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
            print("----------")
      except FileNotFoundError as e:
         print('Could not find file %s' % (args.file))
         return e.errno
      return 0
   else:
      print('Add support for the stored, processed json.')
      return 22

if __name__ == '__main__':
   main()

