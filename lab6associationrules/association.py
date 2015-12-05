#! /usr/local/bin/python3

# CPE 466 Fall 2015
# Lab 6: Association Rule Mining
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import errno
import os
import sys

sys.path.append(os.getcwd())
import lab6

def main():
   # PARSE ARGS
   data_filename = None
   min_sup = None
   min_conf = None
   arg_parser = lab6.get_association_args()
   args = arg_parser.parse_args()

   return 0

if __name__ == '__main__':
   rtn = main()
   sys.exit(rtn)
