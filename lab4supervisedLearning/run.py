#! /usr/local/bin/python3
print("hi")

# CPE 466 Fall 2015
# Lab 4: Supervised Learning
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import os
import sys
import argparse

sys.path.append(os.getcwd())


DESCRIPTION  = 'CPE 466 Lab 4: Supervised Learning.'


def argError(msg):
   if msg:
      print("%s: error: %s" % (os.path.basename(__file__), msg) )
      sys.exit(22)

def buildArgs():
   argParser = argparse.ArgumentParser(prog=sys.argv[0], description=DESCRIPTION)
   argParser.add_argument('-f','--filename',
         action='store',
         metavar='filename',
         help='the file to be parsed, appended with .csv for Comma-Separated',
         required=True)
   return argParser

def main():
   # ARGUMENT PARSING
   argParser = buildArgs()
   args = argParser.parse_args()
   print("----------")

   # CSV PARSING
   if args.filename[-4:] == '.csv':
      try:
         with open(args.filename) as raw_data:
            print('Processing CSV file: %s' % (args.filename))
            print('use csv library here wooooo')
      except OSError as e:
         if e.errno == errno.ENOENT:
            print('Could not find file %s' % (args.file))
            return errno.ENOENT
   else:
      print('Supplied file is not in CSV format: %s' % (args.filename))
      exit(22)

   print("Got here! Bye bye")
   print("----------")

if __name__ == '__main__':
   rtn = main()
   exit(rtn)

