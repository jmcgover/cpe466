# CPE 466 Fall 2015
# Lab 3: PageRank
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu


sys.path.append(os.getcwd())
from graph import Edge
from graph import Graph
from graph import Node
from graph import Parser

class PageRank(object):
    def __init__(self, nodeLabel, edges, initPageRank):
        self.nodeLabel
        self.edges = edges
        self.pageRank = initPageRank
    def __hash__(self):
        return self.nodeLabel.__hash__()
    def getEdges(self):
        return self.edges
    def getNodeLabel(self):
        return self.label

class PageRankCalculator(object):
    def __init__(self, graph):
        self.graph = graph
        self.numNodes = graph.getNumNodes()
        self.
    def calcPageRank():
        return results

class PageRankResults(object):
    def __init__(self, graph):
        self.nodes = dict.fromkeys(graph.getNodesUsed())

