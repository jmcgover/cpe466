#! /usr/local/bin/python3

# CPE 466 Fall 2015
# Lab 4: Supervised Learning
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import math

import errno
import os
import sys

sys.path.append(os.getcwd())
import lab4args

def calc_entropy(allDataRows, possibleValues, classification):
   entropy = 0
   total = len(allDataRows[classification])
   for label in possibleValues[classification]:
      count = allDataRows[classification].count(label)
      prob = float(count)/total
      entropy += prob * math.log(prob, 2)
   entropy *= -1
   return entropy

def calc_info_gain(allDataRows, possibleValues, splitAttrib, classification):
   gain = 0
   total = len(allDataRows[splitAttrib])

   for label in possibleValues[splitAttrib]:
      count = 0
      for item in allDataRows[splitAttrib]:
         if item == label:
            count += 1
      if count != 0 and total != 0:
         prob = float(count/total)
         gain += prob * math.log(prob,2)

   entropy = calc_entropy(allDataRows, possibleValues, classification)
   entropy += gain
   return entropy

# TO DO make a recursive driver for this junk
def gen_tree(allDataRows, possibleValues, attribs, classification):
   # Check for stop condition of only 1 category label
   setSize = len(set(allDataRows[classification]))
   if setSize == 0:
      print("only one category label here!")

   # Check for stop condition of no more attributes to split on. Win by plurality.
   attributes = len(attribs)
   if attributes == 0:
      print("no more attributes to split on!")

   else:
      # Otherwise, recursive step of selecting the splitting attribute and splitting the data.
      gains = {}
      for attribute in attribs:
         if attribute != classification:
            gains[attribute] = calc_info_gain(allDataRows, possibleValues, attribute, classification)

   #   print(gains)
   #   print(max(gains.values()))
      maxGain = max(gains.values())
      for attrib, gain in gains.items():
         if maxGain == gain:
            print("Splitting attribute is....")
            print(attrib)
            # TO DO actual data set splits
            for splitVal in possibleValues[attrib]:
               print(splitVal)
               dataCopy = {}
               for attributes in possibleValues:
                  #   print(attributes)
                  if attributes != attrib:
                     dataCopy[attributes] = []
                     for item, match in zip(allDataRows[attributes], allDataRows[attrib]):
                        if match == splitVal:
                           #        print(item)
                           dataCopy[attributes].append(item)
               print(dataCopy)


def main():
   return 0

if __name__ == '__main__':
   rtn = main()
   sys.exit(rtn)
