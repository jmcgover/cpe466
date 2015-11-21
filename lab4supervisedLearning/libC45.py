# CPE 466 Fall 2015
# Lab 4: Supervised Learning
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

# Contains the implementation of various utility functions that are primarily
# program and function oriented (as opposed to algorithm related).

import argparse
import copy
import csv
import os
import sys

import xml.etree.ElementTree as ElementTree

class Dataset(object):
   def __init__(
         self,
         domain_filename=None, csv_filename=None, restrictions_filename=None,
         dataset=None, attribute=None, value=None
      ):
      self.allDataRows = None
      #self.possibleValues = None
      self.attributes = None
      self.attributeValues = {}
      self.attributeCounts = {}
      self.numValues = None
      self.classAttribute = None
      self.classes = None
      self.dataSize = None
      self.domain = None

      # COPY DATASET
      if dataset:
         assert csv_filename == None
         assert attribute and value
         # "header" stuff
         attributes = copy.deepcopy(dataset.attributes)
         numValues = copy.deepcopy(dataset.numValues)
         classAttribute = copy.deepcopy(dataset.classAttribute)

         possibleNumValues = {}
         #possibleValues = {}
         allDataRows = {}

         for col, val in zip(attributes, numValues):
            possibleNumValues[col] = val
            #possibleValues[col] = []
            allDataRows[col] = []
         allDataRows[classAttribute] = []

         # Calculate length
         length = 0
         for col in dataset.allDataRows:
            if length:
               assert len(dataset.allDataRows[col])
               assert len(dataset.allDataRows[col]) == length
            else:
               length = len(dataset.allDataRows[col])
         dataSize = 0
         if attribute and value:
            # Filter and copy
            for i in range(0, length):
               if dataset.allDataRows[attribute][i] == value:
                  dataSize += 1
                  for col in dataset.allDataRows:
                     allDataRows[col].append(dataset.allDataRows[col][i])
               #else:
               #   print('%s != %s' % (dataset.allDataRows[attribute][i], value))
         else:
            # Simply copy
            print('dataSize: %d', dataSize)
            for i in range(0, dataSize - 1):
               for col in dataset.allDataRows:
                  allDataRows[col].append(dataset.allDataRows[col][i])
         self.domain = dataset.domain
      # BUILD FROM CSV FILE
      if csv_filename:
         assert dataset == None
         # Check for filename extension
         if csv_filename[-4:] != '.csv':

            print('File is not in CSV format: %s' % (csv_filename), file=sys.stderr)
            sys.exit(errno.EINVAL)
         try:
            with open(csv_filename) as file:
               reader = csv.reader(file, delimiter = ',')

               # Process header rows
               attributes = reader.__next__()
               numValues = reader.__next__()
               classAttributeRow = reader.__next__()
               classAttribute = classAttributeRow[0]

               # Create a dictionary with the number of possible
               #     values for each attribute
               # Also sets up dictionary to list what the possible
               #     attribute labels are and store all data
               possibleNumValues = {}
               #possibleValues = {}
               allDataRows = {}

               for col, val in zip(attributes, numValues):
                  possibleNumValues[col] = val
                  #possibleValues[col] = []
                  allDataRows[col] = []

               # Process each CSV row into its own dictionary of attributes
               dataSize = 0
               for row in reader:
                  dataSize += 1
                  for col, item in zip(attributes, row):
                     allDataRows[col].append(item)
                     #if item not in possibleValues[col]:
                     #   possibleValues[col].append(item)

               # Remove the classAttribute label from the attribute list
               #     as well as the attributes with no classifications
               #     or with a val of 0 in the restrictions file
               if restrictions_filename:
                  with open(restrictions_filename) as restrictions_file:
                     restrictions_reader = csv.reader(restrictions_file, delimiter = ',')
                     restrictions = restrictions_reader.__next__()
                     for attribute, restriction_val in zip(attributes, restrictions):
                        if int(restriction_val) == 0:
                           possibleNumValues[attribute] = -1
               attributes.remove(classAttribute)
               removedAttributes = set()
               for attribute in attributes:
                  if int(possibleNumValues[attribute]) <= 0:
                     removedAttributes.add(attribute)
                     del allDataRows[attribute]
                     #del possibleNumValues[attribute]
                     #del possibleValues[attribute]
                     print("Removed %s..." % (attribute))
               for attribute in removedAttributes:
                  attributes.remove(attribute)
               #print(attributes)
               #print(allDataRows)


         except OSError as e:
            if e.errno == errno.ENOENT:
               print('Could not find file %s' % (csv_filename))
               sys.exit(errno.ENOENT)

            else:
               raise e
         except:
            raise
      self.allDataRows = allDataRows
      self.attributes = attributes
      for a in attributes:
         self.attributeValues[a] = set(allDataRows[a])
         self.attributeCounts[a] = {}
         for val in self.attributeValues[a]:
            self.attributeCounts[a][val] = allDataRows[a].count(val)
      self.attributeValues[classAttribute] = set(allDataRows[classAttribute])
      self.attributeCounts[classAttribute] = {}
      for val in self.attributeValues[classAttribute]:
         self.attributeCounts[classAttribute][val] = allDataRows[classAttribute].count(val)
      self.numValues = numValues
      self.classAttribute = classAttribute
      self.classes = set(allDataRows[classAttribute])
      self.dataSize = dataSize
      if not self.domain:
         self.domain = Domain(domain_filename)

   def get_attributes(self):
      return self.attributes
   def get_attributeValues(self, attribute):
      return self.attributeValues[attribute]
   def get_numAttributeValues(self, attribute):
      return len(self.attributeValues[attribute])
   def count_values(self, attribute, value):
      return self.attributeCounts[attribute][value]

   def get_classAttribute(self):
      return self.classAttribute
   def get_classes(self):
      return self.classes
   def get_numClasses(self):
      return len(self.classes)
   def get_mostPluralClass(self):
      max_count = -1
      max_class = None
      for c in self.attributeCounts[self.classAttribute]:
         if self.attributeCounts[self.classAttribute][c] > max_count:
            max_count = self.attributeCounts[self.classAttribute][c]
            max_class = c
      return max_class
   def get_dataSize(self):
      return self.dataSize
   def pr(self, attribute, value):
      return self.count_values(attribute, value) / self.get_dataSize()
   def pr_c(self, c_j):
      num_class_c_j = self.count_values(self.classAttribute, c_j)
      num_examples = self.get_dataSize()
      return  num_class_c_j / num_examples
   def get_num_choice_tuple(self, attribute, value):
      num = None
      choice = None
      print('ATTR: %s VALUE: %s' % (attribute, value))
      try:
         num = self.domain.get_num(attribute, value)
         choice = self.domain.get_choice(attribute, num)
      except KeyError as e:
         choice = self.domain.get_choice(attribute, value)
         num = self.domain.get_num(attribute, choice)
      return (num, choice)

class Domain(object):
   def __init__(self, xml_filename):
      assert(xml_filename)
      tree = ElementTree.parse(xml_filename)
      domain = tree.getroot()
      print(domain.tag)
      assert domain.tag == 'domain'

      self.attributes = set()
      self.num_by_choice = {}
      self.choice_by_num = {}
      for node in domain:
         assert node.tag == 'node'
         assert node.attrib['var']
         attribute = node.attrib['var']

         self.attributes.add(attribute)
         self.num_by_choice[attribute] = {}
         self.choice_by_num[attribute] = {}

         for edge in node:
            assert edge.tag == 'edge'
            assert edge.attrib['num']
            assert edge.attrib['var']
            num = edge.attrib['num']
            choice = edge.attrib['var']

            self.num_by_choice[attribute][choice] = num
            self.choice_by_num[attribute][num] = choice

   def print(self, file=sys.stdout):
      for attribute in self.attributes:
         print("ATTRIBUTE %s" % attribute)
         print("\t%s INDEXED BY NUM" % (attribute))
         for choice in self.num_by_choice[attribute]:
            print('\t\t%s: %s' % (choice, self.num_by_choice[attribute][choice]))
         print("\t%s INDEXED BY CHOICE" % (attribute))
         for num in self.choice_by_num[attribute]:
            print('\t\t%s: %s' % (num, self.choice_by_num[attribute][num]))
   def get_num(self, attribute, choice):
      return self.num_by_choice[attribute][choice]
   def get_choice(self, attribute, num):
      return self.choice_by_num[attribute][num]
   def get_all_nums(self, attribute):
      return self.num_by_choice[attribute]
   def get_all_choices(self, attribute):
      return self.choice_by_num[attribute]

