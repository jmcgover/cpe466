#! /usr/local/bin/python3

# CPE 466 Fall 2015
# Lab 4: Supervised Learning
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import csv
import errno
import math
import os
import random
import sys

import xml.etree.ElementTree as ElementTree

sys.path.append(os.getcwd())
import lib_lab4
from lib_lab4 import getClassifierArgs
from lib_lab4 import getXMLTree

seed = round(math.pow(2, 16))
print(seed)
random.seed(os.urandom(seed))

def print_tree(root):
   print_tree_rec(root, 0)
   return None

def print_tree_rec(node, indents):
   print("%s%s(%s) %s" % ('----'*indents, node.tag, type(node), node.attrib))
   for child in node:
      print_tree_rec(child, indents + 1)
   return None

class Records(object):
   def __init__(self, csv_filename, other=None):
      # DECLARE
      self.attributes = None
      self.classAttribute = None
      self.records = None
      self.numRecords = None
      self.records_name = os.path.splitext(csv_filename)[0]

      if other:
         self.attributes = other.attributes
         self.classAttribute = other.classAttribute
         self.records = other.records
         self.numRecords = other.numRecords
         self.records_name = other.records_name
      else:
         # PARSE
         assert csv_filename[-4:] == '.csv'
         with open(csv_filename) as csv_file:
            # BUILD CSV READER
            reader = csv.reader(csv_file, delimiter = ',')

            # STORE NUM VALUES FOR EACH ATTRIBUTE
            row_attributes = reader.__next__()
            row_numValues = reader.__next__()
            assert len(row_attributes) == len(row_numValues)
            numValues = {}
            attributes = set()
            for attribute,numVals in zip(row_attributes, row_numValues):
               numValues[attribute] = int(numVals)
               if int(numVals) > 0:
                  attributes.add(attribute)

            # GET CLASSIFIER ATTRIBUTE
            row_classAttribute = reader.__next__()
            assert len(row_classAttribute) == 1
            classAttribute = row_classAttribute[0]

            # BUILD A DICT FOR EACH RECORD
            records = []
            for row_record in reader:
               record = {}
               for attribute, value in \
                     zip(row_attributes, row_record):
                  if numValues[attribute] > 0:
                     record[attribute] = value
               records.append(record)

            # ASSIGN VALUES TO OBJECT
            self.attributes = attributes
            self.classAttribute = classAttribute
            self.records = records
            self.numRecords = len(records)

   def __iter__(self):
      return self.records.__iter__()
   def get_record(self, i):
      return self.records[i]
   def get_records(self, i, j):
      return self.records[i:j]
   def clear_records(self):
      self.records = []
   def get_classAttribute(self):
      return self.classAttribute
   def get_newEmptyRecords(self):
      emptyRecords = Records(None, other=self)
      emptyRecords.clear_records()
      return emptyRecords
   def add_record(self, record):
      self.numRecords += 1
      self.records.append(record)
   def pop_record(self, i):
      if len(self.records) > 0:
         self.numRecords -= 1
         return self.records.pop(i)
      return None
   def pop_random_record(self):
      i = None
      i = random.randint(0, self.numRecords - 1)
      return self.records.pop(i)
   def build_randomSubset(self, k):
      newRecords = None
      if k < 0:
         newRecords = self.get_newEmptyRecords()
         newRecords.addRecord(self.pop_random_record())
      if k == 0:
         newRecords = self
      if k < self.numRecords - 1:
         newRecords = self.get_newEmptyRecords()
         i = 0
         while i < k:
            newRecords.addRecord(self.pop_random_record())
            i += 1
      return newRecords

class DecisionTree(object):
   def __init__(self, xml_filename=None, xml_str=None):
      assert xml_filename or str
      self.root = None
      root = None
      if xml_filename:
         assert xml_filename[-4:] == '.xml'
         tree = ElementTree.parse(xml_filename)
         root = tree.getroot()
      else:
         root = ElementTree.fromstring(xml_str)
      self.root = root
   def classify(self, record):
      return self.classify_rec(record, self.root)
   def classify_rec(self, record, element):
      #print("%s: %s" % (element.tag, element.attrib))
      tag = element.tag
      if 'Tree' == tag:
         tree = element
         for node in tree:
            return self.classify_rec(record, node)
      if 'node' == tag:
         node = element
         attribute = node.attrib['var']
         for edge in node:
            num = edge.attrib['num']
            var = edge.attrib['var']
            if record[attribute] == num or record[attribute] == var:
               return self.classify_rec(record, edge)
      if 'edge' == tag:
         edge = element
         for child in edge:
            return self.classify_rec(record, child)
         assert False # WILL ALWAYS LEAD TO DECISION OR NODE
      if 'decision' == tag:
         decision = element
         end = decision.attrib['end']
         choice = decision.attrib['choice']
         num = decision.attrib['num']
         assert int(end) == 1
         return (num, choice)
      # NO CLASSIFICATION
      return None
      #print('WHAT THE FUCK: %s %s' % (tag, record))
      #for child in element:
      #   print("\t%s: %s" % (child.tag, child.attrib))
      ##assert False # SHOULD NEVER REACH HERE -- ONLY ONE

def main():
   # PARSE
   parser = getClassifierArgs()
   args = parser.parse_args()

   # GET FILENAMES
   csv_records_filename = args.csv_file
   xml_dec_tree_filename = args.xml_file

   # PARSE RECORDS
   records = Records(csv_records_filename)
   classAttribute = records.get_classAttribute()

   # PARSE DECISION TREE
   dec_tree = DecisionTree(xml_dec_tree_filename)

   # CLASSIFY RECORDS
   records_total = 0
   records_right = 0
   records_wrong = 0
   real_class = None
   for record in records:
      resulting_classification = dec_tree.classify(record)
      if resulting_classification:
         num, var = resulting_classification
         try:
            real_class = record[classAttribute]
         except KeyError:
            real_class = None
         print("%s ~~> %s %s" % (record[classAttribute], num, var))
         # COUNT STUFF
         records_total += 1
         if real_class:
            if real_class == num or real_class == var:
               records_right += 1
            else:
               records_wrong += 1
   print("%s: %d" % ('Total', records_total))
   print("%s: %d" % ('Right', records_right))
   print("%s: %d" % ('Wrong', records_wrong))
   print("%s: %.3f" % ('Accuracy', records_right/records_total))
   print("%s: %.3f" % ('ErrrRate', records_wrong/records_total))

   # CLASSIFY RECORDS
   return 0

if __name__ == '__main__':
   rtn = main()
   sys.exit(rtn)
