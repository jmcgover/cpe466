# CPE 466 Fall 2015
# Lab 5: Clustering
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import csv
import os
import sys

class Dataset(object):
   def __init__(self, data_filename, header_filename):
      self.datapoints = None
      self.attributes = None
      self.restrictions = None

      # BEGIN READ HEADER FILE
      attributes = None
      with open(header_filename) as header_file:
         csv_reader = csv.reader(header_file, delimiter=',')
         attributes = csv_reader.__next__()
      # END   READ HEADER FILE

      # BEGIN READ DATA FILE
      restrictions = None
      datapoints = []
      with open(data_filename) as data_file:
         csv_reader = csv.reader(data_file, delimiter=',')
         restrictions = csv_reader.__next__()
         assert len(restrictions) == len(attributes)
         for row in csv_reader:
            assert len(row) == len(restrictions)
            datapoint = []
            for i in range(len(restrictions)):
               if restrictions[i] == '1':
                  datapoint.append(float(row[i]))
            datapoints.append(datapoint)
      # END   READ DATA FILE

      self.datapoints = datapoints
      self.attributes = attributes
      self.restrictions = restrictions
   def __iter__(self):
      return self.datapoints.__iter__()

   def get_datapoints(self):
      return self.datapoints
   def get_attributes(self):
      return self.attributes
   def get_restrictions(self):
      return self.restrictions
