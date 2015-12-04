#! /usr/local/bin/python3

# CPE 466 Fall 2015
# Lab 5: Clustering
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import errno
import json
import os
import sys

import collections
from collections import Counter

import itertools
import pprint
import xml.etree.ElementTree as ElementTree


sys.path.append(os.getcwd())
import cluster
from cluster import Dataset
import lab5
from  lab5 import get_header_filename

import distances
from distances import euclidean_distance

pprint.PrettyPrinter(indent=2)

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
   return sum(distances) / (len(c_x), len(c_y))

def centroid_method(distance, c_x, c_y):
   centroid_x = calc_centroid(c_x)
   centroid_y = calc_centroid(c_y)
   return distance(centroid_x, centroid_y)

def wards_methods(distance, c_x, c_y):
   return None

class Agglomerative(object):
   def __init__(self,
         distance = euclidean_distance,
         agglomerate_method = single_link,
         ):
      self.distance = distance
      self.agglomerate_method = agglomerate_method
   def cluster_distance(self, c_x, c_y):
      return self.agglomerate_method(self.distance, c_x, c_y)
   def find_closest_clusters(self, clusters):
      c_s, c_r = None, None
      min_dist = None
      for c_x, c_y in itertools.combinations(clusters, 2):
         dist = self.cluster_distance(c_x, c_y)
         if min_dist == None or dist < min_dist:
            min_dist = dist
            c_s, c_r = c_x, c_y
      return c_s,c_r
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
      all_clusters = []
      for x in D:
         cluster = [x]
         all_clusters.append(cluster)
      pprint.pprint(all_clusters)
      while len(all_clusters) > 1:
         print('--------')
         a,b = self.find_closest_clusters(all_clusters)
         #pprint.pprint(a)
         #pprint.pprint(b)
         all_clusters.remove(a)
         all_clusters.remove(b)
         new_cluster = []
         new_cluster.extend(a)
         new_cluster.extend(b)
         all_clusters.append(new_cluster)
         pprint.pprint(all_clusters)
         #pprint.pprint(new_cluster)
      print('len(all_clusters): {0}'.format(len(all_clusters)))

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
   print('Threshold      : %.3f' % threshold) if threshold else None

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
