# CPE 466 Fall 2015
# Lab 4: Supervised Learning
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

# Contains the implementation of various utility functions that are primarily
# program and function oriented (as opposed to algorithm related).

import argparse
import os
import sys

import xml.etree.ElementTree as ElementTree

# ARGUMENTS
class SmartFormatter(argparse.HelpFormatter):

    def _split_lines(self, text, width):
        # this is the RawTextHelpFormatter._split_lines
        if text.startswith('R|'):
            return text[2:].splitlines()  
        return argparse.HelpFormatter._split_lines(self, text, width)

DESCRIPTION_C45 = 'Task 1: C4.5 Decision Tree induction'
COL_C45 = '90'
def getC45Args():
   # os.environ['COLUMNS'] = COL_C45
   argParser = argparse.ArgumentParser(prog=sys.argv[0], description=DESCRIPTION_C45)
   argParser.add_argument(
         'domain_file', metavar='<domainFile.xml>',
         help='XML file containing the domain description for the dataset,'
         );
   argParser.add_argument(
         'training_file', metavar='<TrainingSetFile.xml>',
         help='input training set CSV file'
         );
   argParser.add_argument(
         'restrictions_file', metavar='<restrictionsFile.txt>', nargs='?', default=None,
         help='TXT file containing a single vector, the size of which is equal to the number of coumns in the dataset without the category variable, where each element is 0 or 1 indicating which attributes of the dataset to use when inducing the decision tree'
         );
   return argParser

DESCRIPTION_CLASSIFIER = 'Task 2: Classification'
COL_CLASSIFIER = '90'
def getClassifierArgs(description=None):
   # os.environ['COLUMNS'] = COL_C45
   if description:
      argParser = argparse.ArgumentParser(prog=sys.argv[0], description=description, formatter_class=SmartFormatter)
   else:
      argParser = argparse.ArgumentParser(prog=sys.argv[0], description=DESCRIPTION_CLASSIFIER, formatter_class=SmartFormatter)
   argParser.add_argument(
         'csv_file', metavar='<CSVFile>',
         help='CSV file of records to be classified and outputs the classification result for each vector'
         );
   argParser.add_argument(
         'xml_file', metavar='<XMLFile>',
         help='XML description of a decision already generated'
         );
   return argParser

DESCRIPTION_VALIDATION = 'Task 3: Evaluation'
COL_VALIDATION = '90'
def getValidationArgs():
   # os.environ['COLUMNS'] = COL_VALIDATION
   argParser = getClassifierArgs(DESCRIPTION_VALIDATION)
   argParser.add_argument(
         'n', metavar='<N>', type=int,
         help='R|specifies how many-fold the cross-validation has to be:\
               \n  N = 0 represents no cross-validation \
               \n    (i.e., use entire training set to construct a single classifier)\
               \n  N = −1 represents all-but-one cross-validation.'
         );
   argParser.add_argument(
         'restrictions_file', metavar='<restrictionsFile.txt>', nargs='?', default=None,
         help='TXT file containing a single vector, the size of which is equal to the number of coumns in the dataset without the category variable, where each element is 0 or 1 indicating which attributes of the dataset to use when inducing the decision tree'
         );
   return argParser

def getDataRows():
   allDataRows = None
   return allDataRows

def getXMLTree(filename):
   tree = None
   tree = ElementTree.parse(filename)
   return tree_root
