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

from xml.dom import minidom

sys.path.append(os.getcwd())
import libC45 as C45
import lib_lab4
from lib_lab4 import getCSVData
from libC45 import Dataset

def entropy(D, A=None):
   sum = 0.0
   if A:
      for v_j in D.get_attributeValues(A):
         D_j = Dataset(None, None, None, D, A, v_j)
         sum += D_j.get_dataSize() / D.get_dataSize() * entropy(D_j)
      #print('Entropy[%s]: %.3f' % (A, sum))
   else:
      for c_j in D.get_classes():
         if D.pr_c(c_j):
            sum += D.pr_c(c_j) * math.log(D.pr_c(c_j), 2)
      sum = -1 * sum
      #print('Entropy: %.3f' % (sum))
   return sum

def normalizer(D, A):
   sum = 0.0
   for v in D.get_attributeValues(A):
      D_j = Dataset(None, None, None, D, A, v)
      pr_A = D_j.get_dataSize() / D.get_dataSize()
      sum +=  pr_A * math.log(pr_A, 2)
   sum = -1 * sum
   #print('Normalizer: %.3f' % (sum))
   return sum

def select_splitting_attribute_ratio(D, A, threshold):
   p_0 = entropy(D)
   p = {}
   gain = {}
   gainRatio = {}
   for A_i in D.get_attributes():
      p[A_i] = entropy(D, A_i)
      gain[A_i] = p_0 - p[A_i]
      gainRatio[A_i] = gain[A_i] / normalizer(D, A_i)
   max_gain_ratio = -10
   best = None
   for A_i in gain:
      #print('%-30s: %.3f > %.3f' % (A_i, gainRatio[A_i] , max_gain_ratio))
      if gainRatio[A_i] > max_gain_ratio:
         max_gain_ratio = gainRatio[A_i]
         best = A_i
   #print(p_0)
   #print(p)
   #print(gain)
   #print(gainRatio)
   #print('max_ratio: %.3f best: %s gain %.3f' % (max_gain_ratio, best, gain[best]))
   if gain[best] <= threshold:
      best = None
   return best

def select_splitting_attribute_default(D, A, threshold):
   p_0 = entropy(D)
   p = {}
   gain = {}
   for A_i in D.get_attributes():
      p[A_i] = entropy(D, A_i)
      gain[A_i] = p_0 - p[A_i]
   max_gain = threshold
   best = None
   for A_i in gain:
      if gain[A_i] > max_gain:
         max_gain = gain[A_i]
         best = A_i
   #print(p_0)
   #print(p)
   #print(gain)
   #print('max: %.3f best: %s' % (max_gain, best))
   return best

class DecisionTreeBuilder(object):
   def __init__(self,
         domain_filename, csv_filename, restrictions_filename = None, 
         ratio=False
      ):
      print('~' * 20)
      print(csv_filename)
      print(restrictions_filename)
      print(ratio)
      self.tree = None
      self.tree_name = csv_filename[:-4]
      self.restricted = False
      if restrictions_filename:
         print('FUCKING RESTRICTED')
         self.restricted = True
      else:
         print('NOT RESTRICTED?!?! %s' % restrictions_filename)
      print('~' * 20)
      self.select_splitting_attribute = select_splitting_attribute_default
      if ratio:
         self.select_splitting_attribute = select_splitting_attribute_ratio
      self.trainingSet = Dataset(domain_filename, csv_filename, restrictions_filename)

   def decision_tree_rec(self, D, A, T, threshold):
      assert D.get_numClasses() > 0
      if D.get_numClasses() == 1:
         print('make T a leaf node with labeled with c');
         decision = ElementTree.SubElement(T, 'decision')
         decision.set('end', '1')
         decision.set('choice', D.get_classes().pop())
      elif len(A) == 0:
         print('make T a leaf node labeled with the most frequent class')
         decision = ElementTree.SubElement(T, 'decision')
         decision.set('end', '1')
         decision.set('choice', D.get_mostPluralClass())
      else:
         print('contains examples belonging to a mixture of classes')
         A_split = self.select_splitting_attribute(D, A, threshold)
         print('SPLITTING ON %s: ', A_split)
         #A_split = select_splitting_attribute_ratio(D, A, threshold)
         #print('SPLITTING ON RATIO %s: ', A_split)
         if A_split == None:
            decision = ElementTree.SubElement(T, 'decision')
            decision.set('end', '1')
            decision.set('choice', D.get_mostPluralClass())
         else:
            node = ElementTree.SubElement(T, 'node')
            node.set('var', A_split)
            A_A_split = set()
            for a in A:
               if a != A:
                  A_A_split.add(a)
            for v in D.get_attributeValues(A_split):
               D_v = Dataset(None, None, None, D, A_split, v)
               if D_v.get_dataSize() > 0:
                  edge = ElementTree.SubElement(node, 'edge')
                  edge.set('var', v)
                  self.decision_tree_rec(D_v, A_A_split, edge, threshold)
   def build_tree(self, threshold):
      self.tree = Element('Tree')
      self.tree.set('name',self.tree_name)
      allAttributes = self.trainingSet.get_attributes()
      self.decision_tree_rec(self.trainingSet, allAttributes, self.tree, threshold)
      return self.tree
   def get_tree(self):
      return self.tree
   def get_xml(self, indent='   '):
      return minidom.parseString(
            ElementTree.tostring(self.tree)).toprettyxml(indent=indent)
   def print_tree(self, file=sys.stdout, indent='   '):
      xml_str = self.get_xml(indent)
      print(xml_str, file=file)
      return xml_str
   def save_tree(self, file=None, indent='   '):
      if file:
         return self.print_tree(file, indent)
      else:
         xml_filename = self.tree_name
         if self.restricted:
            xml_filename += '_restricted'
         xml_filename += '.xml'
         with open(self.tree_name + '.xml', 'w') as save_file:
            xml_str = self.print_tree(save_file, indent)
         return xml_str


def main():
   parser = lib_lab4.getC45Args()
   args = parser.parse_args()
   domain_filename = args.domain_file
   csv_training_filename = args.training_file
   restrictions_filename = args.restrictions_file
   threshold = .001

   print('Processing CSV file %s' % (csv_training_filename), end='')
   if restrictions_filename:
      print(' with restriction file %s' % restrictions_filename, end='')
   print('...')
   builder = \
      DecisionTreeBuilder(domain_filename, csv_training_filename, restrictions_filename)
   print('done!')
   print('Building Decision Tree via C4.5...')
   tree = builder.build_tree(threshold)
   print('done!')
   builder.print_tree()
   builder.save_tree()
   return 0

if __name__ == '__main__':
   rtn = main()
   sys.exit(rtn)
