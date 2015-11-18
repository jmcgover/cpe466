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

def main():
   parser = lib_lab4.getValidationArgs()
   parser.parse_args()
   return 0

if __name__ == '__main__':
   rtn = main()
   sys.exit(rtn)
