#! /usr/local/bin/python3

# CPE 466 Fall 2015
# Lab 5: Clustering
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import ast
import errno
import json
import os
import sys

import collections
from collections import Counter

import itertools
import pprint

import xml.etree.ElementTree as ElementTree
from   xml.etree.ElementTree import Element
from xml.dom import minidom


sys.path.append(os.getcwd())

import cluster
from cluster import Dataset
from cluster import print_stats
from cluster import squared_error
from cluster import sum_squared_error

import lab5
from  lab5 import get_header_filename
from  lab5 import get_distance_metric

import distances
from distances import euclidean_distance

pprint.PrettyPrinter(indent=2)

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

pre_computed = {}
def calc_all_distances(distance, c_x, c_y):
   distances = []
   for x in c_x:
      for y in c_y:
         dist = None
         if (x,y) in pre_computed:
            dist = pre_computed[(x,y)]
         else:
            dist = distance(x,y)
            pre_computed[(x,y)] = dist
         distances.append(dist)
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

def calc_centroids(clusters):
   centroids = []
   for c in clusters:
      centroids.append(calc_centroid(c))
   return centroids

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

def get_xml(tree, indent='   '):
   return minidom.parseString(
         ElementTree.tostring(tree)).toprettyxml(indent=indent)
def print_tree(tree, file=sys.stdout, indent='   '):
   xml_str = get_xml(tree, indent)
   print(xml_str, file=file)
   return xml_str
def save_tree(tree, file, indent='   '):
   return print_tree(tree, file, indent)

class Agglomerative(object):
   def __init__(self,
         distance = euclidean_distance,
         agglomerate_method = single_link,
         ):
      self.distance = distance
      self.agglomerate_method = agglomerate_method
      self.tree = None
   def calc_stats(self, centroid, cluster):
      distances = []
      for x in cluster:
         distances.append(self.distance(x, centroid))
      return max(distances), min(distances), sum(distances)/len(distances),\
            squared_error(centroid, cluster, self.distance)
   def cluster_distance(self, c_x, c_y):
      return self.agglomerate_method(self.distance, c_x, c_y)
   def find_closest_clusters(self, clusters):
      s, r = None, None
      min_dist = None
      for i in range(len(clusters)):
         for j in range(len(clusters)):
            dist = self.cluster_distance(clusters[i], clusters[j])
            if i != j and (min_dist == None or dist < min_dist):
               min_dist = dist
               s,r = i,j
      return min_dist, (s, r)
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
      all_elements = []

      # INITIALIZE CLUSTERS
      for x in D:
         cluster = [x]
         all_clusters.append(cluster)
         leaf_cluster = ElementTree.Element('leaf')
         leaf_cluster.set('height', '0.0')
         leaf_cluster.set('data',x)
         all_elements.append(leaf_cluster)
      #pprint.pprint(all_clusters)
      #for e in all_elements:
      #   pprint.pprint(e.attrib)
      while len(all_clusters) > 1:
         #print('--------')

         # FIND CLOSEST CLUSTERS
         min_dist,(s,r) = self.find_closest_clusters(all_clusters)

         # EXTRACT CLUSTERS
         a = all_clusters[s]
         b = all_clusters[r]
         all_clusters.remove(a)
         all_clusters.remove(b)
         a_elem = all_elements[s]
         b_elem = all_elements[r]
         all_elements.remove(a_elem)
         all_elements.remove(b_elem)

         # AGGLOMERATE
         new_cluster = []
         new_cluster.extend(a)
         new_cluster.extend(b)
         new_element = ElementTree.Element('node')
         new_element.set('height', '%.3f' % min_dist)
         new_element.append(a_elem)
         new_element.append(b_elem)
         #pprint.pprint(new_cluster)

         # ADD THE NEW CLUSTER
         all_clusters.append(new_cluster)
         all_elements.append(new_element)
         #pprint.pprint(all_clusters)
      self.tree = all_elements[0]
      self.tree.tag = 'tree'
      return self.tree

def get_all_clusters(tree):
   clusters = []
   get_all_clusters_rec(clusters, tree)
   return clusters
def get_all_clusters_rec(clusters, element):
   for e in element:
      if e.tag == 'leaf':
         clusters.append(e.attrib['data'])
      else:
         get_all_clusters_rec(clusters, e)

def get_branches_rec(branches, element, threshold):
   for e in element:
      if e.tag == 'tree' or e.tag == 'node':
         if float(e.attrib['height']) < threshold:
            branches.append(e)
         else:
            get_branches_rec(branches, e, threshold)

def get_clusters(tree, threshold):
   centroids = None
   clusters  = []
   branches = []
   trimmed_tree = ElementTree.Element('trimmed_tree')
   trimmed_tree.set('threshold', '%.3f' % threshold)

   get_branches_rec(branches, tree, threshold)
   for b in branches:
      trimmed_tree.append(b)
   for stem in branches:
      clusters.append(get_all_clusters(stem))
   centroids = calc_centroids(clusters)

   return trimmed_tree, centroids, clusters

def get_cluster_distance(args):
   if args.single:
      return single_link
   if args.complete:
      return complete_link
   if args.average:
      return average_link
   if args.centroid:
      return centroid_method

def main():

   # PARSE ARGS
   data_filename = None
   header_filename = None
   threshold = None
   distance_metric = None
   cluster_distance = None

   parser = lab5.get_hierarchical_args()
   args = parser.parse_args()
   data_filename = args.csv_filename
   if args.header_filename:
      header_filename = args.header_filename
   elif args.infer_header:
      header_filename = get_header_filename(data_filename)
   threshold = args.threshold
   distance_metric = get_distance_metric(args)
   cluster_distance = get_cluster_distance(args)
   print('Data   Filename: %s' % data_filename)
   print('Header Filename: %s' % header_filename)
   print('Threshold      : %.3f' % threshold) if threshold else None

   # READ DATA
   dataset = Dataset(data_filename, header_filename)
   #for d in dataset:
   #   print(d)

   # CALC AGGLOMERATIVE
   agglomerative = Agglomerative(distance_metric, cluster_distance)

   dendrogram = agglomerative.agglomerative(dataset)
   all_clusters = get_all_clusters(dendrogram)
   if threshold:
      trimmed_tree, centroids, clusters = get_clusters(dendrogram, threshold)
      for c in clusters:
         print(c)
      print(len(clusters))
      print_tree(trimmed_tree)
      num_datapoints = print_stats(dataset, agglomerative, clusters, centroids)
      print('Datapoints clustered: %d' % num_datapoints)
      print('Datapoints total    : %d' % dataset.size())
   else:
      print_tree(dendrogram)

   return 0

if __name__ == '__main__':
   rtn = main()
   sys.exit(rtn)
