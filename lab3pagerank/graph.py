# CPE 466 Fall 2015
# Lab 3: PageRank
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import bisect
import resource
import sys
# from networkx import read_gml
import locale

#print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000)
locale.setlocale(locale.LC_ALL, 'en_US.utf8')

class EfficientGraph():
    def __init__(self, maxNodeNum):
        self.nodes = [{}] * (maxNodeNum + 1)
        #self.nodes = dict.fromkeys(range(maxNodeNum + 1))
        self.numEdges = 0
        self.nodesUsed = {}
    def __iter__(self):
        return self.nodes.__iter__()
    def __str__(self):
        return self.nodes.__str__()
    def addEdge(self, node, edgeLabel, neighbor):
        if node  >= len(self.nodes):
            while node >= len(self.nodes) - 1:
                self.nodes.append({})
        self.nodes[node][neighbor] = edgeLabel
        self.numEdges += 1
        self.nodesUsed[node] = True
        self.nodesUsed[neighbor] = True

    def getNumNodes(self):
        return len(self.nodesUsed)
    def getNumEdges(self):
        return self.numEdges
    def getNodesUsed(self):
        return self.nodesUsed
    def getNodeEdges(self, node):
        return self.nodes[int(node)]
    def getNodeNeighbors(self, node):
        try:
            return self.nodes[node]
        except IndexError as err:
            return None

class Graph(object):
    def __init__(self, sortNeighbors=True, maxNodeNum=None):
        self.nodes = {}
        self.numNodes = 0
        self.numEdges = 0
        self.nodesUsed = {}
        if sortNeighbors:
            self.nodeList = []
    def __iter__(self):
        return sorted(self.nodes.keys()).__iter__()
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
            newNode = None
            if hasattr(self, 'nodeList'): # If memory isn't an issue
                newNode = Node(node, sortNeighbors=True)
                bisect.insort(self.nodeList, newNode)
            else:
                newNode = Node(node)
            self.nodes[node] = newNode
        if neighbor not in self.nodes:
            newNode = None
            if hasattr(self, 'nodeList'): # If memory isn't an issue
                newNode = Node(neighbor, sortNeighbors=True)
                bisect.insort(self.nodeList, newNode)
            else:
                newNode = Node(neighbor)
            self.nodes[neighbor] = newNode
        self.nodes[node].addEdge(neighbor, edgeLabel)
        self.numEdges += 1
        self.nodesUsed[node] = True
        self.nodesUsed[neighbor] = True
    def containsNode(self, node):
        return node in self.nodes
    def getNodeList(self):
        if self.nodeList:
            return self.nodeList
        else:
            return self.nodes.keys()
    def getNode(self, node):
        return self.nodes[node]
    def getNodes(self):
        return self.nodes
    def getNumNodes(self):
        return len(self.nodes)
    def getNumEdges(self):
        return self.numEdges
    def getNodeEdges(self, node):
        return self.nodes[node]
    def getNodesUsed(self):
        return self.nodesUsed
    def getNodeNeighbors(self, node):
        try:
            return self.nodes[node].getNeighbors()
        except KeyError as err:
            print("%s" % node)
            raise err

class Node(object):
    def __init__(self, label, sortNeighbors=False):
        self.label = label
        self.edges = {}
        if sortNeighbors:
            self.neighborList = []

    def __cmp__(self, other):
        return self.label.__cmp__(other.label)

    def __lt__(self, other):
        return self.label.__lt__(other.label)

    def __eq__(self, other):
        return self.label.__eq__(other) or self.label.__eq__(other.label)

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

    def __hash__(self):
        return self.label.__hash__()

    def addEdge(self, neighbor, edgeLabel):
        if neighbor not in self.edges:
            if hasattr(self, 'neighborList'):
                bisect.insort(self.neighborList, neighbor)
            self.edges[neighbor] = edgeLabel

    def getLabel(self):
        return self.label
    def getEdge(self, neighbor):
        return self.neighbors[neighbor]
    def getEdges(self):
        return self.edges
    def getNeighbors(self):
        return self.edges

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

class Parser(object):
    commentChars = {'#' : True}
    def __init__(self, file, csv=False, gml=False, txt=False, graph=None, quiet=False, initialSize=None, undirected=False):
        if graph:
            self.graph = graph
        else :
            if not csv and not gml and not txt:
                raise AttributeError('Must be either csv or gml or txt, not none.')
            if (csv and gml) or (csv and txt) or (gml and txt):
                raise AttributeError('Must be either csv or gml or txt, not both.')
            self.file = file
            self.linesParsed = 0
            self.csv = csv
            self.gml = gml
            self.txt = txt
            self.graph = None
            self.quiet = quiet
            self.initialSize = initialSize
            self.undirected = undirected
    def parseGraph(self):
        try:
            self.file.readable()
        except IOError as err:
            raise  IOError('File is not readable. Please ensure that it is open.')
        if self.txt:
            # TXT Parsing goes here
            maxNodeNum = 0
            if not self.initialSize:
                if not self.quiet:
                    print('Calculating max node....')
                for line in self.file:
                    tuple = self._getTupleTXT(line)
                    if tuple :
                        self.initialSize = max(maxNodeNum, int(tuple[0]), int(tuple[1]))
            if not self.quiet:
                print('Max node is %d.' % self.initialSize)
            self.graph = EfficientGraph(self.initialSize)
            #self.graph = Graph(sortNeighbors=False, maxNodeNum=self.initialSize)
            self.file.seek(0)
            self.linesParsed = 0;
            for line in self.file:
                tuple = self._getTupleTXT(line)
                if tuple:
                    if len(tuple) == 2:
                        a = int(tuple[0])
                        b = int(tuple[1])
                        self.graph.addEdge(a, 1, b)
                    elif len(tuple) == 3:
                        a = int(tuple[0])
                        b = int(tuple[1])
                        a_b = int(tuple[2])
                        if a_b > 0:
                            self.graph.addEdge(a, 1, b)
                    else:
                        print('FOUND TUPLE LEN %d' % (len(tuple)), file=sys.stderr)
                if not self.quiet and self.linesParsed % 1000000 == 0:
                    print("%s: (nodes:%s, edges:%s) graph:%s nodes:%s [%s]:%s total:%s" % (
                        locale.format( "%d", self.linesParsed, grouping=True),
                        locale.format( "%d", self.graph.getNumNodes(), grouping=True),
                        locale.format( "%d", self.graph.getNumEdges(), grouping=True),
                        locale.format( "%d", sys.getsizeof(self.graph), grouping=True),
                        locale.format( "%d", sys.getsizeof(self.graph.nodes), grouping=True),
                        locale.format( "%d", a, grouping=True),
                        locale.format( "%d", sys.getsizeof(self.graph.nodes[a]), grouping=True),
                        locale.format( "%d", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, grouping=True)))
        if self.csv:
            # CSV Parsing goes here
            if not self.quiet:
                print('Parsing CSV..')
            self.graph = Graph()
            for line in self.file:
                tuple = self._getTupleCSV(line)
                if tuple and len(tuple) >= 4:
                    a = tuple[0]
                    b = tuple[2]
                    a_b = int(tuple[1])
                    b_a = int(tuple[3])
                    if a_b == 0 and b_a == 0:
                        self.graph.addEdge(a, True, b)
                        if self.undirected:
                            print('ADDING UNDIRECTED')
                            self.graph.addEdge(b, 1, a)
                    else:
                        if a_b > b_a:
                            self.graph.addEdge(a, 1, b)
                        else:
                            self.graph.addEdge(b, 1, a)
                        

        if self.gml:
            # GML Parsing goes here
            # self.graph = read_gml
            if not self.quiet:
                print('Parsing GML..')
        return self.graph
    def _getTupleTXT(self, line):
        tuple = None
        if line:
            self.linesParsed += 1
            if line[0] not in self.commentChars:
                line = line.strip()
                tuple = line.split()
        return tuple
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
