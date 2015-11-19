#! /usr/local/bin/python3

# CPE 466 Fall 2015
# Lab 4: Supervised Learning
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import errno
import os
import sys

import xml.etree.ElementTree as ElementTree

sys.path.append(os.getcwd())
import lib_lab4
from lib_lab4 import getClassifierArgs
from lib_lab4 import getXMLTree

def print_tree(root):
   print_tree_rec(root, 0)
   return None

def print_tree_rec(node, indents):
   print("%s%s(%s) %s" % ('----'*indents, node.tag, type(node), node.attrib))
   for child in node:
      print_tree_rec(child, indents + 1)
   return None



def main():
   # PARSE
   parser = getClassifierArgs()
   args = parser.parse_args()

   # GET FILENAMES
   csv_records_filename = args.csv_file
   xml_dec_tree_filename = args.xml_file

   # PARSE DECISION TREE
   dec_tree = ElementTree.parse(xml_dec_tree_filename)
   dec_tree_root = dec_tree.getroot()

   # TODO REMOVE DEBUG
   # Printing Tree
   print(dec_tree_root)
   for n in dec_tree_root:
      print("%s %s" % (n.tag, n.attrib))
   print_tree(dec_tree_root)

   # PARSE RECORDS

   # CLASSIFY RECORDS
   return 0

if __name__ == '__main__':
   rtn = main()
   sys.exit(rtn)
