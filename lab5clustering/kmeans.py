#! /usr/local/bin/python3

# CPE 466 Fall 2015
# Lab 5: Clustering
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import errno
import os
import random
import sys

import distances
from distances import euclidean_distance

sys.path.append(os.getcwd())
import cluster
from cluster import Dataset
import lab5
from  lab5 import get_header_filename

class KMeans(object):
   def __init__(self, distance = euclidean_distance):
      self.distance = distance

   def select_initial_clusters(self, D, k):
      clusters = []
      rand_indices = random.sample(range(D.size()), k)
      for i in rand_indices:
         clusters.append(D.get_single_point(i))
      return clusters

   def disk_k_means(self, D, k):
      assert k < D.size(), 'k(%d) is larger than data(%d)' % (k, D.size())
      clusters = None
      means = self.select_initial_clusters(D, k)
      repeat = True
      while repeat:
         family = k*[None]
         num_points = k*[0]
         clusters = k*[[]]
         print('family: %s' % family)
         print('num_points: %s' % num_points)
         print('clusters: %s' % clusters)
         repeat = False
      return clusters

def main():

   # PARSE ARGS
   data_filename = None
   header_filename = None
   k = None

   parser = lab5.get_k_means_args()
   args = parser.parse_args()
   data_filename = args.csv_filename
   if args.header_filename:
      header_filename = args.header_filename
   elif args.infer_header:
      header_filename = get_header_filename(data_filename)
   k = args.k
   print('Data   Filename: %s' % data_filename)
   print('Header Filename: %s' % header_filename)
   print('k              : %d' % k)

   # READ DATA
   dataset = Dataset(data_filename, header_filename)
   print(dataset.get_attributes())
   for d in dataset.get_datapoints():
      print(d)
   k_means = KMeans()
   k_means.disk_k_means(dataset, k)

   return 0

if __name__ == '__main__':
   rtn = main()
   sys.exit(rtn)
