#! /usr/local/bin/python3

# CPE 466 Fall 2015
# Lab 5: Clustering
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import errno
import os
import sys

sys.path.append(os.getcwd())
import lab5
from  lab5 import get_header_filename

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
   else:
      header_filename = get_header_filename(data_filename)
   threshold = args.threshold
   print('Data   Filename: %s' % data_filename)
   print('Header Filename: %s' % header_filename)
   print('Threshold      : %.3f' % threshold)

   # READ DATA
   return 0

if __name__ == '__main__':
   rtn = main()
   sys.exit(rtn)
