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
from graph import Graph
from graph import Node
from graph import Edge

WIDTH=100
INDENT=4
DESCRIPTION="CPE 466 Lab 3: PageRank."

def buildPageRankArgs():
    argParser = argparse.ArgumentParser(prog=sys.argv[0], description=DESCRIPTION)
    return argParser

def main():
    argParser = buildPageRankArgs()

if __name__ == '__main__':
    rtn = main()
    exit(rtn)
