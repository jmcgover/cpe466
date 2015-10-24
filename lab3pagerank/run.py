#!/usr/bin/python

# CPE 466 Fall 2015
# Lab 3: PageRank
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import errno
import json
import operator
import os
import pickle
import sys
import textwrap
import time
import argparse

sys.path.append(os.getcwd())
from graph import Edge
from graph import Graph
from graph import Node
from graph import Parser

from pagerank import PageRank
from pagerank import PageRankCalculator
from pagerank import PageRankResults

WIDTH=50
INDENT=4
DESCRIPTION  = 'CPE 466 Lab 3: PageRank.'
DESCRIPTION += ''

DEF_DAMPER = .5
DEF_EPSILON = .0000001
DEF_LIMIT = 257

FMT_STR = '%s,%s,%s,%s,%s,%s,%s,%s'
TIMING_HEADER = FMT_STR % ('Filename','d','e','Nodes','Edges','ParseTime(sec)','PageRankTime(s)','Iterations')

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
    argParser.add_argument('-v', '--verbose',
            action='store_true',
            default=False,
            help='verobsely prints the details of each iteration')
    argParser.add_argument('-t', '--time',
            action='store_true',
            default=False,
            help='outputs time only to stdout in csv format')
    argParser.add_argument('-H', '--header',
            action='store_false',
            default=True,
            help='suppresses the timing header')
    argParser.add_argument('-e', '--epsilon',
            action='store',
            type=float,
            default=DEF_EPSILON,
            metavar='num',
            required=False,
            help='epsilon to stop the iteration at (default is %f)' % DEF_EPSILON)
    argParser.add_argument('-d', '--damper',
            action='store',
            type=float,
            default=DEF_DAMPER,
            metavar='prob',
            required=False,
            help='damper constant (default is %f)' % DEF_DAMPER)
    argParser.add_argument('-l', '--limit',
            action='store',
            type=float,
            default=DEF_LIMIT,
            metavar='prob',
            required=False,
            help='limit of top results to show (defualt is %d)' % DEF_LIMIT)
    argParser.add_argument('-u', '--undirected',
            action='store_true',
            default=False,
            help='interpret weights with two 0\'s as undirected (default is directed)')
    # PRINTING
    argParser.add_argument('-E','--print-edges',
            action='store',
            metavar='label1,label2,...',
            help='prints the edges for the node labels given')
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
    argParser.add_argument('-P', '--parse-only',
            action='store_true',
            default=False,
            help='only parses the graph, doesn\'t PageRank')
    argParser.add_argument('-R', '--print-results-stats',
            action='store_true',
            default=False,
            help='print statistics of the results')
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
    group.add_argument('-x', '--txt',
            action='store_true',
            default=False,
            help='forces White-Space Separated file interpretation')
    return argParser

def main():
    argParser = buildPageRankArgs()
    args = argParser.parse_args()
    quiet = args.quiet or args.time
    verbose = args.verbose
    d = DEF_DAMPER
    epsilon = DEF_EPSILON
    if args.damper:
        d = float(args.damper)
        if d < 0 or d > 1:
            print('%f is not in [0,1]',file=sys.stderr)
            return errno.EINVAL
    if args.epsilon:
        epsilon = float(args.epsilon)
    # FIGURE OUT FILETYPE
    if not args.csv and not args.gml and not args.txt:
        args.csv  = args.filename[-4:] == '.csv'
        args.gml  = args.filename[-4:] == '.gml'
        args.txt  = args.filename[-4:] == '.txt'
        if not args.csv and not args.gml and not args.txt:
            print('Please provide a file ending in .csv or .gml \
                    or provide the appropriate command line flags', file=sys.stderr)
            argParser.print_help()
            return errno.EINVAL

    # PARSE GRAPH
    graph = None
    parseTime = None
    calcTime = None
    t0 = None
    t1 = None
    try:
        graphParser = None
        with open(args.filename, 'r') as raw_graph_file:
            if not quiet:
                print('Parsing %s...' % (args.filename), file=sys.stderr)
            graphParser = Parser(raw_graph_file, csv=args.csv, gml=args.gml, txt=args.txt, quiet=args.quiet, initialSize=args.initial_size)
            t0 = time.time()
            graph = graphParser.parseGraph()
            t1 = time.time()
            parseTime = t1 - t0
            if not quiet:
                print('Done parsing %s.' % (args.filename), file=sys.stderr)
    except OSError as e:
        if e.errno == errno.ENOENT:
            print('Could not find graph file "%s"' % (args.filename), file=sys.stderr)
            return errno.ENOENT
        else:
            print('Some other error occured with %s' % (args.filename), file=sys.stderr)
            raise e
    if graph == None:
        print('Soemthing fucky happened and graph is empty', file=sys.stderr)
        return errno.EINVAL
    # DO STUFF WITH IT

    # PRINT
    # NODE
    if args.print_edges:
        if not quiet:
            print('-' * WIDTH, file=sys.stderr)
            print('Printing EDGES', file=sys.stderr)
            print('-' * WIDTH, file=sys.stderr)
        for n in args.print_edges.split(','):
            print(graph.getNodeEdges(n), file=sys.stderr)

    if args.print_nodes:
        if not quiet:
            print('-' * WIDTH, file=sys.stderr)
            print('Printing NODES', file=sys.stderr)
            print('-' * WIDTH, file=sys.stderr)
        for n in graph.getNodes():
            print(len(graph.getNodeNeighbors(n)), graph.getNode(n), file=sys.stderr,)
    # GRAPH
    if args.print_graph:
        if not quiet:
            print('-' * WIDTH, file=sys.stderr)
            print('Printing GRAPH', file=sys.stderr)
            print('-' * WIDTH, file=sys.stderr)
        print(graph, file=sys.stderr)
    if args.print_stats:
        if not quiet:
            print('-' * WIDTH, file=sys.stderr)
            print('Printing STATS', file=sys.stderr)
            print('-' * WIDTH, file=sys.stderr)
        print("Nodes: %d" % (graph.getNumNodes()), file=sys.stderr)
        print("Edges: %d" % (graph.getNumEdges()), file=sys.stderr)
    if not quiet:
        print('-' * WIDTH, file=sys.stderr)
    if not args.parse_only:
        calculator = PageRankCalculator(graph, verbose=args.verbose)
        if not quiet:
            print('CALCULATING PageRank', file=sys.stderr)
            print('-' * WIDTH, file=sys.stderr)
        t0 = time.time()
        results = calculator.calcPageRank(d, epsilon)
        t1 = time.time()
        calcTime = t1 - t0
        ranks = results.getPageRanks()
        if not args.time:
            print('-' * WIDTH, file=sys.stderr)
            print('Filename\t: %s' % args.filename, file=sys.stderr)
            print('Damping\t: %.9f' % d, file=sys.stderr)
            print('Epsilon\t: %.9f' % epsilon, file=sys.stderr)
            print("%s\t%s\t%s" % ("RESULT", "NODE", "PageRank"), file=sys.stderr)
            i = 1
            for r in ranks:
                print('%d\t%s\t%.9f' % (i, r.getNodeLabel(), r.getPageRank()), file=sys.stderr)
                if args.limit > 0 and i == args.limit:
                    break
                i += 1
            print('-' * WIDTH, file=sys.stderr)
        print(TIMING_HEADER)
        print(FMT_STR % (args.filename,d,epsilon,graph.getNumNodes(),graph.getNumEdges(),parseTime,calcTime,results.getIterations()))
    else:
        print(TIMING_HEADER)
        print(FMT_STR % (args.filename,d,epsilon,graph.getNumNodes(),graph.getNumEdges(),parseTime,calcTime,None))

    # PAGE RANK

if __name__ == '__main__':
    rtn = main()
    exit(rtn)
