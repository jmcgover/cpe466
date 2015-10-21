import bisect

class Graph(object):
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def addEdge(self, node, edgeLabel, neighbor):
        if a not in self.nodes:
            self.nodes[node] = {}
        self.nodes[node].addEdge(neighbor, edgeLabel)
        self.edges.append(Edge(node, edgeLabel, neighbor))
    def containsNode(self, node):
        return node in self.nodes

class Parser(object):
    def __init__(self, file, csv=True, gml=False, graph=None):
        if not csv and not gml:
            raise AttributeError('Must be either csv or gml, not neither.')
        if csv and gml:
            raise AttributeError('Must be either csv or gml, not both.')
        self.file = file
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
        if self.csv:
            # CSV Parsing goes here
            print('will parse CSV')
        if self.gml:
            # GML Parsing goes here
            print('will parse GML')
        return self.graph

class Node(object):
    def __init__(self, label):
        self.label = label
        self.edges = {}
        self.neighbors = []

    def hash(self):
        return self.label.hash()

    def addEdge(self, neighbor, edgeLabel):
        bisect.insort(self.neighbors, neighbor)
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
