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

from pagerank import PageRank
from pagerank import PageRankCalculator
from pagerank import PageRankResults

WIDTH=100
INDENT=4
DESCRIPTION  = 'CPE 466 Lab 3: PageRank.'
DESCRIPTION += ''

def buildPageRankArgs():
    argParser = argparse.ArgumentParser(prog=sys.argv[0], description=DESCRIPTION)
    argParser.add_argument('-f','--filename',
            action='store',
            metavar='filename',
            help='the file to be parsed, appended with .csv for Comma-Separated Value or .gml for Graph Markup Language',
            required=True)
    argParser.add_argument('-q', '--quiet',
            action='store_true',
            default=False,
            help='quiets the pretty part of the output but errors are still printed')
    argParser.add_argument('-N', '--print-nodes',
            action='store_true',
            default=False,
            help='prints the nodes in the graph with edges each as a row of pseudo-JSON objects')
    argParser.add_argument('-G', '--print-graph',
            action='store_true',
            default=False,
            help='prints the graph as a single pseudo-JSON object')
    argParser.add_argument('-S', '--print-stats',
            action='store_true',
            default=False,
            help='prints numebrs relevant to the graph')
    # Initial size of graph
    argParser.add_argument('-i', '--initial-size',
            action='store',
            type=int,
            nargs='?',
            metavar='nodes',
            required=False,
            help='number of nodes to initialize the matrix with')
    # Sub Group of Filetype
    group = argParser.add_mutually_exclusive_group()
    group.add_argument('-c', '--csv',
            action='store_true',
            default=False,
            help='forces Comma-Separated Value file interpretation')
    group.add_argument('-g', '--gml',
            action='store_true',
            default=False,
            help='forces Graph Markup Language file interpretation')
    group.add_argument('-t', '--txt',
            action='store_true',
            default=False,
            help='forces White-Space Separated file interpretation')
    return argParser

def main():
    argParser = buildPageRankArgs()
    args = argParser.parse_args()
    quiet = args.quiet
    # FIGURE OUT FILETYPE
    if not args.csv and not args.gml and not args.txt:
        args.csv  = args.filename[-4:] == '.csv'
        args.gml  = args.filename[-4:] == '.gml'
        args.txt  = args.filename[-4:] == '.txt'
        if not args.csv and not args.gml and not args.txt:
            print('Please provide a file ending in .csv or .gml \
                    or provide the appropriate command line flags')
            argParser.print_help()
            return errno.EINVAL

    # PARSE GRAPH
    graph = None
    try:
        graphParser = None
        with open(args.filename, 'r') as raw_graph_file:
            if not quiet:
                print('Parsing %s...' % (args.filename))
            graphParser = Parser(raw_graph_file, csv=args.csv, gml=args.gml, txt=args.txt, quiet=args.quiet, initialSize=args.initial_size)
            graph = graphParser.parseGraph()
            if not quiet:
                print('Done parsing %s.' % (args.filename))
    except OSError as e:
        if e.errno == errno.ENOENT:
            print('Could not find graph file "%s"' % (args.filename))
            return errno.ENOENT
        else:
            print('Some other error occured with %s' % (args.filename))
            raise e
    if graph == None:
        print('Soemthing fucky happened and graph is empty', file=sys.stderr)
        return errno.EINVAL
    # DO STUFF WITH IT

    # PRINT
    # NODE
    if args.print_nodes:
        if not quiet:
            print('-' * WIDTH)
            print('Printing NODES')
            print('-' * WIDTH)
        for n in graph:
            print(n)
    # GRAPH
    if args.print_graph:
        if not quiet:
            print('-' * WIDTH)
            print('Printing GRAPH')
            print('-' * WIDTH)
        print(graph)
    if args.print_stats:
        if not quiet:
            print('-' * WIDTH)
            print('Printing STATS')
            print('-' * WIDTH)
        print("Nodes: %d" % (graph.getNumNodes()))
        print("Edges: %d" % (graph.getNumEdges()))
    if not quiet:
        print('-' * WIDTH)

    # PAGE RANK

if __name__ == '__main__':
    rtn = main()
    exit(rtn)
