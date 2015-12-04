# CPE 466 Fall 2015
# Lab 5: Clustering
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import collections
import csv
import os
import sys

from collections import defaultdict

class Dataset(object):
   def __init__(self, data_filename, header_filename=None):
      # DECLARE MEMBER VARS
      self.datapoints = None
      self.dim = None
      self.restrictions = None
      self.unused_data = None

      # BEGIN READ HEADER FILE
      self.attributes = None
      attributes = None
      if header_filename:
         with open(header_filename) as header_file:
            csv_reader = csv.reader(header_file, delimiter=',')
            attributes = csv_reader.__next__()
      self.attributes = attributes
      # END   READ HEADER FILE

      # BEGIN READ DATA FILE
      restrictions = None
      datapoints = []
      unused_data = defaultdict(list)
      unused_data_tracked = False
      dim = 0
      with open(data_filename) as data_file:
         csv_reader = csv.reader(data_file, delimiter=',')
         restrictions = csv_reader.__next__()
         for r in restrictions:
            if r == '1':
               dim += 1
         assert not attributes or len(restrictions) == len(attributes)
         for row in csv_reader:
            if len(row):
               assert len(row) == len(restrictions), \
                  'row(%d) != restrictions(%d) %s' % \
                  (len(row), len(restrictions), data_filename)
               datapoint = []
               unused_info = []
               for i in range(len(restrictions)):
                  if restrictions[i] == '1':
                     datapoint.append(float(row[i]))
                  else:
                     unused_data_tracked = True
                     unused_info.append(row[i])
               datapoint = tuple(datapoint)
               if len(unused_info):
                  unused_info = tuple(unused_info)
               datapoints.append(datapoint)
               unused_data[datapoint].append(unused_info)
      # END   READ DATA FILE

      # ASSIGN MEMBER VARS
      self.datapoints = datapoints
      if unused_data_tracked:
         self.unused_data = unused_data
      self.dim = dim
      self.restrictions = restrictions
   def __iter__(self):
      return self.datapoints.__iter__()

   def get_datapoints(self):
      return self.datapoints
   def size(self):
      return len(self.datapoints)
   def dimensions(self):
      return self.dim
   def get_single_point(self, ndx):
      assert ndx < self.size()
      return self.datapoints[ndx]
   def get_attributes(self):
      return self.attributes
   def get_restrictions(self):
      return self.restrictions
