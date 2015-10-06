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

DESCRIPTION="CPE 466 Lab 2: Information Retrieval from Digital Democracy."

def buildArguments():
    argParser = argparse.ArgumentParser(prog=sys.argv[0], description=DESCRIPTION)
    argParser.add_argument('-f','--file',
           action='store',
           metavar='file',
           help='the file to be parsed, appended with .json for JSON and .???? for the ???',
           required=True)

    return argParser

def main():
    argParser = buildArguments()
    args = argParser.parse_args()
    filename = args.file
    if filename[-4:] != 'json':
        print('This better be a json file!')
    with open(filename) as corpus:
        try:
            json.load(corpus)
        except ValueError as err:
            print('Failed to load %s as json file' % filename)
            return 22
        print('Sucessfully loaded %s' % filename)
    return 0

if __name__ == '__main__':
    main()
