#! /usr/local/bin/python3

# CPE 466 Fall 2015
# Lab 4: Supervised Learning
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import math

import errno
import os
import sys

import xml.etree.ElementTree as ElementTree
from   xml.etree.ElementTree import Element

sys.path.append(os.getcwd())
import libC45 as C45
import lib_lab4
from lib_lab4 import getCSVData
from libC45 import Dataset

def entropy(D):
   print('ENTROPPPYYY')

def select_splitting_attribute(A, D, threshold):
   p_0 = entropy(D)

def build_tree(trainingSet, threshold):
   root = Element('Tree')
   allAttributes = trainingSet.get_attributes()
   decision_tree_rec(trainingSet, allAttributes, root, threshold)
   return root

def decision_tree_rec(D, A, T, threshold):
   classes = D.get_classes()
   assert len(classes) > 0
   if len(classes) == 1:
      print('make T a leaf node with labeled with c');
   elif len(A) == 0:
      print('make T a leaf node labeled with the most frequent class')
   else:
      print('contains examples belonging to a mixture of classes')
      split_attrib = select_splitting_attribute(D, A, threshold)

def main():
   parser = lib_lab4.getC45Args()
   args = parser.parse_args()
   csv_training_filename = args.training_file
   threshold = .001

   print('Processing CSV file %s...' % (csv_training_filename))
   trainingSet = Dataset(csv_filename = csv_training_filename)
   print('done!')
   print("----------")
   print('Generating Decision Tree via C4.5...')
   root = build_tree(trainingSet, threshold)
   print('done!')
   print('Copying trainingset...')
   newTrainingSet = Dataset(dataset=trainingSet, attribute='Vote', value='Obama')
   return 0

if __name__ == '__main__':
   rtn = main()
   sys.exit(rtn)
