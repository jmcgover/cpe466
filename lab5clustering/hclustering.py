#! /usr/local/bin/python3

# CPE 466 Fall 2015
# Lab 5: Clustering
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import errno
import json
import os
import sys

import xml.etree.ElementTree as ElementTree

sys.path.append(os.getcwd())
import cluster
from cluster import Dataset
import lab5
from  lab5 import get_header_filename

import distances
from distances import euclidean_distance

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

def calc_all_distances(distance, c_x, c_y):
   distances = set()
   for x in c_x:
      for y in c_y:
         distances.add(distance(x,y))
   return distances

def calc_centroid(cluster):
   sum = None
   for x in cluster:
      if sum:
         assert len(sum) == len(x)
         sum = [a + b for a,b in zip(sum, x)]
      else:
         sum = x
   return [s / len(cluster) for s in sum]

def single_link(distance, c_x, c_y):
   distances = calc_all_distances(distance, c_x, c_y)
   return min(distances)

def complete_link(distance, c_x, c_y):
   distances = calc_all_distances(distance, c_x, c_y)
   return max(distances)

def average_link(distance, c_x, c_y):
   distances = calc_all_distances(distance, c_x, c_y)
   return avg(distances)

def centroid_method(distance, c_x, c_y):
   centroid_x = calc_centroid(c_x)
   centroid_y = calc_centroid(c_y)
   return distance(centroid_x, centroid_y)

def wards_methods(distance, c_x, c_y):
   return None

class Agglomerative(object):
   def __init__(self,
         distance = euclidean_distance,
         cluster_distance = single_link,
         ):
      self.distance = distance
      self.cluster_distance = cluster_distance
   def d(self, c_x, c_y):
      return self.cluster_distance(self.distance, c_x, c_y)
      return 0
   def arg_min(self, d):
      (s,r) = (-1,-1)
      min_dist = None
      for j in d.keys():
         for k in d[j].keys():
            if min_dist == None or d[j][k] < min_dist:
               min_dist = d[j][k]
               s,r = (j,k)
      return (s,r)
   def agglomerative(self, D):

def main():

   # PARSE ARGS
   data_filename = None
   header_filename = None
   threshold = None

   parser = lab5.get_hierarchical_args()
   args = parser.parse_args()
   data_filename = args.csv_filename
   if args.header_filename:
      header_filename = args.header_filename
   elif args.infer_header:
      header_filename = get_header_filename(data_filename)
   threshold = args.threshold
   print('Data   Filename: %s' % data_filename)
   print('Header Filename: %s' % header_filename)
   print('Threshold      : %.3f' % threshold)

   # READ DATA
   dataset = Dataset(data_filename, header_filename)
   #for d in dataset:
   #   print(d)

   # CALC AGGLOMERATIVE
   agglomerative = Agglomerative()

   agglomerative.agglomerative(dataset)

   return 0

if __name__ == '__main__':
   rtn = main()
   sys.exit(rtn)
