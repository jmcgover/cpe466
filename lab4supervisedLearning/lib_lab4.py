# CPE 466 Fall 2015
# Lab 4: Supervised Learning
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

# Contains the implementation of various utility functions that are primarily
# program and function oriented (as opposed to algorithm related).

import argparse
import os
import sys

DESCRIPTION_C45 = 'Task 1: C4.5 Decision Tree induction'
COL_C45 = '90'
def getC45Args():
   # os.environ['COLUMNS'] = COL_C45
   argParser = argparse.ArgumentParser(prog=sys.argv[0], description=DESCRIPTION_C45)
   argParser.add_argument(
         'domain_file', metavar='<domainFile.xml>',
         help='the name of the XML file containing the domain description for the dataset,'
         );
   argParser.add_argument(
         'training_file', metavar='<TrainingSetFile.xml>',
         help='the name of the input training set file'
         );
   argParser.add_argument(
         'domain_file', metavar='<restrictionsFile.txt>', nargs='?', default=None,
         help='the name of a text file containing a single vector, the size of which is equal to the number of coumns in the dataset without the category variable, where each element is 0 or 1 indicating which attributes of the dataset to use when inducing the decision tree'
         );
   return argParser
