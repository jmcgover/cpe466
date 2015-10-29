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
    argParser.add_argument('-p', '--pickle',
            action='store_true',
            help='saves the parsed collection to the original filename.pickle')
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
    argParser.add_argument('-V', '--validate',
            action='store_true',
            help='go through the special validation game we built')
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
