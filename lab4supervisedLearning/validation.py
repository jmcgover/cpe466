#! /usr/local/bin/python3

# CPE 466 Fall 2015
# Lab 4: Supervised Learning
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import errno
import os
import sys

sys.path.append(os.getcwd())
import lib_lab4
import libC45
import induceC45
import classifier

from libC45 import Dataset
from induceC45 import DecisionTreeBuilder
from classifier import Records
from classifier import DecisionTree

def main():
   parser = lib_lab4.getValidationArgs()
   args = parser.parse_args()

   domain_filename = args.domain_file
   csv_training_filename = args.training_file
   restrictions_filename = args.restrictions_file
   threshold = .001

   # BULD DECISION TREE
   builder = \
      DecisionTreeBuilder(domain_filename, csv_training_filename, restrictions_filename)
   builder.build_tree(threshold)

   # PARSE DECISION TREE
   dec_tree = DecisionTree(None, xml_str=builder.get_xml())

   # GET RECORDS
   records = Records(csv_training_filename)
   classAttribute = records.get_classAttribute()

   # CLASSIFY RECORDS
   records_total = 0
   records_right = 0
   records_wrong = 0
   real_class = None
   for record in records:
      resulting_classification = dec_tree.classify(record)
      if resulting_classification:
         num, var = resulting_classification
         try:
            real_class = record[classAttribute]
         except KeyError:
            real_class = None
         print("%s ~~> %s %s" % (record[classAttribute], num, var))
         # COUNT STUFF
         records_total += 1
         if real_class:
            if real_class == num or real_class == var:
               records_right += 1
            else:
               records_wrong += 1
   print("%s: %d" % ('Total', records_total))
   print("%s: %d" % ('Right', records_right))
   print("%s: %d" % ('Wrong', records_wrong))
   print("%s: %.3f" % ('Accuracy', records_right/records_total))
   print("%s: %.3f" % ('ErrrRate', records_wrong/records_total))

   return 0

if __name__ == '__main__':
   rtn = main()
   sys.exit(rtn)
