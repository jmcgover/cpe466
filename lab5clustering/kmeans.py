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

def main():
   parser = lab5.get_k_means_args()
   args = parser.parse_args()
   return 0


if __name__ == '__main__':
   rtn = main()
   sys.exit(rtn)
