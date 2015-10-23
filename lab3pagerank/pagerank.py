# CPE 466 Fall 2015
# Lab 3: PageRank
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu


import gc
import os
import sys
sys.path.append(os.getcwd())
from graph import Edge
from graph import Graph
from graph import Node
from graph import Parser

class PageRank(object):
    def __init__(self, nodeLabel, edges, pageRank):
        self.nodeLabel = nodeLabel
        self.edges = edges
        self.pageRank = pageRank
    def __hash__(self):
        return self.nodeLabel.__hash__()
    def __lt__(self, other):
        return self.pageRank < other.pageRank
    def __str__(self):
        return "%s: %f" % (self.nodeLabel, self.pageRank)
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
        for node in self.pageRanks:
            self.pageRanks[node] = PageRank(node, self.graph.getNodeEdges(node), 1.0/self.numNodes)
        print(self.pageRanks)
    def __iter__(self):
        return self.pageRanks.__iter__()

    def updatePageRanks(self, d):
        newPageRanks = dict.fromkeys(self.pageRanks)
        pageRank = None
        self.maxDelta = 0
        for node in self.graph.getNodesUsed():
            pageRank = (1 - d) / self.numNodes
            neighbors = self.graph.getNodeNeighbors(node)
            for neighbor in neighbors:
                d * self.pageRanks[neighbor].getPageRank() / len(neighbors)
            newPageRanks[node] = PageRank(node, self.graph.getNodeEdges(node), pageRank)
            self.maxDelta = max(self.maxDelta, (newPageRanks[node].getPageRank() - self.pageRanks[node].getPageRank()))
        self.pageRanks = newPageRanks
        gc.collect()

    def getMaxDelta(self):
        return self.maxDelta
    def getPageRank(self, node):
        return self.pageRanks[node]

class PageRankCalculator(object):
    def __init__(self, graph):
        self.graph = graph
        self.numNodes = graph.getNumNodes()
    def calcPageRank(self, d, epsilon):
        results = PageRankResults(self.graph)
        while results.getMaxDelta() == None or results.getMaxDelta() > epsilon:
            results.updatePageRanks(d)
        return results




