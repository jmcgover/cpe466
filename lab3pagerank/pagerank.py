# CPE 466 Fall 2015
# Lab 3: PageRank
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu


import bisect
import gc
import os
import sys
sys.path.append(os.getcwd())
from graph import Edge
from graph import Graph
from graph import Node
from graph import Parser

class PageRank(object):
    def __init__(self, nodeLabel, pageRank):
        self.nodeLabel = nodeLabel
        self.pageRank = pageRank
    def __hash__(self):
        return self.nodeLabel.__hash__()
    def __cmp__(self, other):
        return self.pageRank.__cmp__(other.pageRank)
    def __lt__(self, other):
        return self.pageRank > other.pageRank
    def __str__(self):
        return "%s\t%f" % (self.nodeLabel, self.pageRank)
    def getEdges(self):
        return self.edges
    def getNodeLabel(self):
        return self.nodeLabel
    def getPageRank(self):
        return self.pageRank

class PageRankResults(object):
    def __init__(self, graph):
        self.graph = graph
        self.numNodes = graph.getNumNodes()
        self.pageRanks = dict.fromkeys(graph.getNodesUsed())
        self.maxDelta = None
        self.iterations = 0
        for node in self.pageRanks:
            self.pageRanks[node] = PageRank(node, 1.0/self.numNodes)

    def updatePageRanks(self, d):
        newPageRanks = dict.fromkeys(self.pageRanks)
        pageRank = None
        self.maxDelta = 0
        for node in self.graph.getNodesUsed():
            newPageRank = (1-d)/self.numNodes
            neighbors = self.graph.getNodeNeighbors(node)
            for neighbor in neighbors:
                newPageRank += d * self.pageRanks[neighbor].getPageRank()
            newPageRanks[node] = PageRank(node, newPageRank);
            oldPageRank = self.pageRanks[node].getPageRank()
            self.maxDelta = max(self.maxDelta, abs(newPageRank - oldPageRank))
        self.pageRanks = newPageRanks
        self.iterations += 1
        gc.collect()

    def getMaxDelta(self):
        return self.maxDelta
    def getIterations(self):
        return self.iterations
    def getPageRank(self, node):
        return self.pageRanks[node]
    def getPageRanks(self):
        sortedRanks = []
        for node,rank in self.pageRanks.items():
            bisect.insort(sortedRanks, rank)
        return sortedRanks

class PageRankCalculator(object):
    def __init__(self, graph):
        self.graph = graph
        self.numNodes = graph.getNumNodes()
    def calcPageRank(self, d, epsilon):
        results = PageRankResults(self.graph)
        while results.getMaxDelta() == None or results.getMaxDelta() > epsilon:
            results.updatePageRanks(d)
        return results




