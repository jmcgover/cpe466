# CPE 466 Fall 2015
# Lab 3: PageRank
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import bisect
# from networkx import read_gml

class Graph(object):
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.nodeList = []
    def __iter__(self):
        return self.nodeList.__iter__()
    def __str__(self):
        str = "{"
        first = True
        for n in self:
            if not first:
                str += ','
            else:
                first = False
            str += "%s" % n
        str += "}"
        return str

    def addEdge(self, node, edgeLabel, neighbor):
        if node not in self.nodes:
            newNode = Node(node)
            self.nodes[node] = newNode
            bisect.insort(self.nodeList, newNode)
        self.nodes[node].addEdge(neighbor, edgeLabel)
        self.edges.append(Edge(node, edgeLabel, neighbor))
    def containsNode(self, node):
        return node in self.nodes
    def getNodeList(self):
        return self.nodeList

class Parser(object):
    commentChars = {'#' : True}
    def __init__(self, file, csv=True, gml=False, graph=None):
        if not csv and not gml:
            raise AttributeError('Must be either csv or gml, not neither.')
        if csv and gml:
            raise AttributeError('Must be either csv or gml, not both.')
        self.file = file
        self.linesParsed = 0
        self.csv = csv
        self.gml = gml
        self.graph = None
    def parseGraph(self):
        try:
            self.file.readable()
        except IOError as err:
            raise  IOError('File is not readable. Please ensure that it is open.')
        if not self.graph:
            self.graph = Graph()
        if self.txt:
            # TXT Parsing goes here
            for line in self.file:
                tuple = self._getTupleCSV(line)
                a = tuple[0]
                b = tuple[1]
                self.graph.addEdge(a, True, b)
                self.graph.addEdge(b, True, a)
        if self.csv:
            # CSV Parsing goes here
            for line in self.file:
                tuple = self._getTupleCSV(line)
                if tuple and len(tuple) == 4:
                    a = tuple[0]
                    b = tuple[2]
                    a_b = int(tuple[1])
                    b_a = int(tuple[3])
                    if a_b == 0 and b_a == 0:
                        self.graph.addEdge(a, True, b)
                        self.graph.addEdge(b, True, a)
                    else:
                        if a_b > 0:
                            self.graph.addEdge(a, a_b, b)
                        if b_a > 0:
                            self.graph.addEdge(b, b_a, a)
        if self.gml:
            # GML Parsing goes here
            # self.graph = read_gml
            print('Parsing GML..')
        return self.graph
    def _getTupleTXT(self, line):
        tuple = None
        if line:
            self.linesParsed += 1
            if line[0] not in self.commentChars:
                line = line.strip()
                tuple = line.split()
                for i in range(0, len(tuple)):
                    tuple[i] = tuple[i].strip().strip('"')
    def _getTupleCSV(self, line):
        tuple = None
        if line:
            self.linesParsed += 1
            if line[0] not in self.commentChars:
                line = line.strip()
                tuple = line.split(',')
                for i in range(0, len(tuple)):
                    tuple[i] = tuple[i].strip().strip('"')
        return tuple

class Node(object):
    def __init__(self, label):
        self.label = label
        self.edges = {}
        self.neighborList = []

    def __cmp__(self, other):
        return self.label.__cmp__(other.label)

    def __lt__(self, other):
        return self.label.__lt__(other.label)

    def __str__(self):
        str = "{%s: " % self.label
        first = True
        for e in self.neighborList:
            if not first:
                str += ','
            else:
                first = False
            str  += '{%s: %s}' % (e, self.edges[e])
        str += '}'
        return str

    def hash(self):
        return self.label.hash()

    def addEdge(self, neighbor, edgeLabel):
        if neighbor not in  self.edges:
            bisect.insort(self.neighborList, neighbor)
            self.edges[neighbor] = edgeLabel

    def getLabel(self):
        return self.label
    def getEdge(self, neighbor):
        return self.neighbors[neighbor]
    def getEdges(self):
        return self.edges
    def getNeighbors(self):
        return self.neighbors

class Edge(object):
    def __init__(self, node, label, neighbor):
        self.node = node
        self.label = label
        self.neighbor = neighbor

    def getNode(self):
        return self.node
    def getLabel(self):
        return self.label
    def getNeighbor(self):
        return self.neighbor
