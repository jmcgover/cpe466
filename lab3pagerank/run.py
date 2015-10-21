#!/usr/bin/python

# CPE 466 Fall 2015
# Lab 3: PageRank
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import errno
import json
import os
import pickle
import sys
import textwrap
import argparse

sys.path.append(os.getcwd())
from graph import Edge
from graph import Graph
from graph import Node
from graph import Parser

WIDTH=100
INDENT=4
DESCRIPTION="CPE 466 Lab 3: PageRank."

def buildPageRankArgs():
    argParser = argparse.ArgumentParser(prog=sys.argv[0], description=DESCRIPTION)
    argParser.add_argument('-f','--filename',
            action='store',
            metavar='filename',
            help='the file to be parsed, appended with .csv for Comma-Separated Value or .gml for Graph Markup Language',
            required=True)
    group = argParser.add_mutually_exclusive_group()
    group.add_argument('-c', '--csv',
            action='store_true',
            default=False,
            help='forces Comma-Separated Value file interpretation')
    group.add_argument('-g', '--gml',
            action='store_true',
            default=False,
            help='forces Graph Markup Language file interpretation')
    return argParser

def main():
    argParser = buildPageRankArgs()
    args = argParser.parse_args()
    # FIGURE OUT FILETYPE
    if not args.csv and not args.gml:
        args.csv  = args.filename[-4:] == '.csv'
        args.gml  = args.filename[-4:] == '.gml'
        if not args.csv and not args.gml:
            print('Please provide a file ending in .csv or .gml \
                    or provide the appropriate command line flags')
            argParser.print_help()
            return errno.EINVAL

    # PARSE GRAPH
    graph = None
    try:
        graphParser = None
        with open(args.filename) as raw_graph_file:
            print('Parsing %s' % (args.filename))
            graphParser = Parser(raw_graph_file, csv=args.csv, gml=args.gml)
            graph = graphParser.parseGraph()
    except OSError as e:
        if e.errno == errno.ENOENT:
            print('Could not find graph file "%s"' % (args.filename))
            return errno.ENOENT

if __name__ == '__main__':
    rtn = main()
    exit(rtn)
