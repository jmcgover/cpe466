# CPE 466 Fall 2015
# Lab 5: Clustering
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import csv
import os
import sys

class Dataset(object):
   def __init__(self, data_filename, header_filename=None):
      # DECLARE MEMBER VARS
      self.datapoints = None
      self.dim = None
      self.restrictions = None

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
      dim = 0
      with open(data_filename) as data_file:
         csv_reader = csv.reader(data_file, delimiter=',')
         restrictions = csv_reader.__next__()
         for r in restrictions:
            if r == '1':
               dim += 1
         assert not attributes or len(restrictions) == len(attributes)
         for row in csv_reader:
            assert len(row) == len(restrictions)
            datapoint = []
            for i in range(len(restrictions)):
               if restrictions[i] == '1':
                  datapoint.append(float(row[i]))
            datapoints.append(datapoint)
      # END   READ DATA FILE

      # ASSIGN MEMBER VARS
      self.datapoints = datapoints
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
