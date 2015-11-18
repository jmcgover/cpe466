# CPE 466 Fall 2015
# Lab 4: Supervised Learning
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import argparse
import os
import sys

DESCRIPTION_C45 = 'Task 1: C4.5 Decision Tree induction'
def getC45Args():
   argParser = argparse.ArgumentParser(prog=sys.argv[0], description=DESCRIPTION_C45)
   return argParser
