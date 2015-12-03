#! /usr/local/bin/python3

# CPE 466 Fall 2015
# Lab 5: Clustering
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import copy
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

def squared_error(mean, cluster, distance):
   error = 0.0
   for x in cluster:
      error += distance(x, mean)
   return error

def sum_squared_error(k, means, clusters, distance):
   error = 0.0
   for j in range(k):
      error += squared_error(means[j], clusters[j], distance)
   return error

def count_reassignments(prev_clusters, clusters):
   reassignments = None;
   if prev_clusters:
      reassignments = 0;
      for prev,cur in zip(prev_clusters, clusters):
         for p in prev:
            if p not in cur:
               reassignments += 1
   print('REASSIGNMENTS: %s' % reassignments)
   return reassignments

def calc_centroid_changes(prev_centroids, centroids, distance):
   change = None
   if prev_centroids:
      change = 0.0
      for prev,cur in zip(prev_centroids, centroids):
         change += distance(prev, cur)
   print('CENTROID_DELT: %s' % change)
   return change

class KMeans(object):
   def __init__(self,
         distance = euclidean_distance,
         centroid_change_threshold=.0000001,
         ss_error_threshold=.0000001):
      self.distance = distance
      self.prev_clusters = None
      self.prev_means    = None
      self.prev_ss_error = None
      self.centroid_change_threshold = centroid_change_threshold
      self.ss_error_threshold = ss_error_threshold

   def select_initial_clusters(self, D, k):
      clusters = []
      rand_indices = random.sample(range(D.size()), k)
      for i in rand_indices:
         clusters.append(D.get_single_point(i))
      return clusters

   def arg_min(self, k, x, means):
      min_arg = -1
      min_dist = None
      for i in range(k):
         dist = self.distance(x, means[i])
         if min_dist == None or dist < min_dist:
            min_dist = dist
            min_arg = i
      return min_arg

   def stopping_criteria(self, k, means, clusters):
      # First Iteration
      if clusters == None:
         return True

      # Following iterations
      criteria = True

      reassignments = count_reassignments(self.prev_clusters, clusters)
      centroid_change = calc_centroid_changes(self.prev_means, means, self.distance)
      ss_error = sum_squared_error(k, means, clusters, self.distance)

      if self.prev_clusters and reassignments == 0:
         print('Reassignments: %d' % reassignments)
         criteria = False
      if self.prev_means and centroid_change < self.centroid_change_threshold:
         print('centroid_change: %.3f' % centroid_change)
         criteria = False
      if self.prev_ss_error and ss_error < self.ss_error_threshold:
         print('ss_error: %.3f' % ss_error)
         criteria = False

      self.prev_clusters = copy.deepcopy(clusters)
      self.prev_means = copy.deepcopy(means)
      self.prev_ss_error = ss_error

      #print('STOPPING CRITERIA: %s' % (criteria))

      return criteria

   def disk_k_means(self, D, k):
      assert k < D.size(), 'k(%d) is larger than data(%d)' % (k, D.size())
      clusters = None
      means = self.select_initial_clusters(D, k)
      repeat = True
      while self.stopping_criteria(k, means, clusters) == True:
         print('calculating')
         family = [D.dimensions()*[0] for j in range(k)]# family of vectors of size dim(D)
         num_points = [0 for j in range(k)]             # number of points in each cluster
         clusters = [[] for j in range(k)]              # actual clusters
         #print('k: %d' % k)
         #print('family: %s' % family)
         #print('num_points: %s' % num_points)
         #print('clusters: %s' % clusters)
         for x in D:
            j = self.arg_min(k, x, means)
            clusters[j].append(x)
            family[j] = [a + b for a,b in zip(family[j], x)]
            num_points[j] += 1
         for j in range(k):
            if num_points[j]:
               means[j] = [s / num_points[j] for s in family[j]]
      return means, clusters

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

   # CALC K MEANS
   k_means = KMeans()
   centroids, clusters = k_means.disk_k_means(dataset, k)
   num = 0
   for j,centroid,cluster in zip(range(k),centroids,clusters):
      print("cluster[%d] len: %d centroid: %s" % (j, len(cluster), centroid))
      num += len(cluster)
   assert num == dataset.size(), 'num(%d) != D.size(%d)' % (num, dataset.size())

   return 0

if __name__ == '__main__':
   rtn = main()
   sys.exit(rtn)
