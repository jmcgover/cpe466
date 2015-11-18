#! /usr/local/bin/python3

# CPE 466 Fall 2015
# Lab 4: Supervised Learning
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import os
import sys
import argparse
import csv

from c45 import calc_entropy, calc_info_gain, gen_tree

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
            reader = csv.reader(raw_data, delimiter = ',')

            # Start processing header rows in the CSV
            attribs = reader.__next__()
            numValues = reader.__next__()
            classAttrib = reader.__next__()
            classification = classAttrib[0]
#            print(classification)

            # Create a dictionary with the number of possible
            # values for each attribute
            # Also sets up dictionary to list what the possible
            # attribute labels are and store all data
            possibleNumValues = {}
            possibleValues = {}
            allDataRows = {}

            for col, val in zip(attribs, numValues):
               possibleNumValues[col] = val
               possibleValues[col] = []
               allDataRows[col] = []

            # Process each CSV row into its own dictionary of attributes
            for row in reader:
               for col, item in zip(attribs, row):
                  allDataRows[col].append(item)
                  if item not in possibleValues[col]:
                     possibleValues[col].append(item)

            # Remove the classification label from the attribute list
            attribs.remove(classification)
# Debug print statements.....
#            print("----------")
#            print(allDataRows)
#            print(possibleNumValues)
#            print(possibleValues)
            print('CSV file %s processed' % (args.filename))
            print("----------")
            print('Generating Decision Tree via C4.5')

            # Entropy Calculation examples
            print('TEST SHIT BELOW need to finish making the recursive driver for splitting')
            print(calc_entropy(allDataRows, possibleValues, classification))
            print(calc_info_gain(allDataRows, possibleValues, 'Gender', classification))
            print(calc_info_gain(allDataRows, possibleValues, 'Age', classification))
            gen_tree(allDataRows, possibleValues, attribs, classification)


      except OSError as e:
         if e.errno == errno.ENOENT:
            print('Could not find file %s' % (args.file))
            return errno.ENOENT
   else:
      print('Supplied file is not in CSV format: %s' % (args.filename))
      exit(22)

   print("----------")

if __name__ == '__main__':
   rtn = main()
   exit(rtn)

