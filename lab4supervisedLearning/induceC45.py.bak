#! /usr/local/bin/python3

# CPE 466 Fall 2015
# Lab 4: Supervised Learning
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import math
import copy

import errno
import os
import sys

sys.path.append(os.getcwd())
import lib_lab4

def calc_entropy(allDataRows, possibleValues, classification):
   entropy = 0
   total = len(allDataRows[classification])
   for label in possibleValues[classification]:
      count = allDataRows[classification].count(label)
      if count != 0 and total != 0:
         prob = float(count/total)
         entropy += prob * math.log(prob, 2)
   entropy *= -1
   return entropy

def calc_info_gain(allDataRows, possibleValues, splitAttrib, classification):
   print(".....echoing splitting attribute.... %s" % splitAttrib)
   entropy = 0
   total = len(allDataRows[splitAttrib])

   for label in possibleValues[splitAttrib]:
      print(label)
      gain = 0
      for classLabel in possibleValues[classification]:
         classCount = 0
         count = 0
         for item, classify in zip(allDataRows[splitAttrib], allDataRows[classification]):
            if item == label:
               classCount += 1
               if classify == classLabel:
                  count += 1
         if count != 0 and classCount != 0:
            prob = float(count/classCount)
            gain += prob * math.log(prob,2)
         print("%s %s : ((%d/%d) * math.log (%d/%d))" % (label, classLabel, count,classCount,count,classCount))
      entropy += float(classCount/total) * (-1 * gain)
#      print("(%d/%d) * (-1 * %f)" % (classCount,total,gain))
      print("current running sum of entropy %f" % entropy)

   entropy = -entropy
   print(calc_entropy(allDataRows, possibleValues, classification))
   entropy += calc_entropy(allDataRows, possibleValues, classification)
   return entropy

# TO DO make a recursive driver for this junk
def gen_tree(allDataRows, possibleValues, attribs, classification):
   # Check for stop condition of only 1 category label
   setSize = len(set(allDataRows[classification]))
#   print("set size of classification labels: %d" % setSize)
   attributes = len(attribs)
#   print("number of attributes %d" % attributes)

   if setSize == 1:
      print("Only one label - classify vote as: %s" % allDataRows[classification][0])
      return

   # Check for stop condition of no more attributes to split on. Win by plurality.
   elif attributes == 1:
      print("no more attributes to split on!")
      print(set(allDataRows[classification]))
      return

   else:
      # Otherwise, recursive step of selecting the splitting attribute and splitting the data.
      gains = {}
      for attribute in attribs:
         if attribute != classification:
            gains[attribute] = calc_info_gain(allDataRows, possibleValues, attribute, classification)

      print(gains)
 #     print(max(gains.values()))
      maxGain = max(gains.values())
      for attrib, gain in gains.items():
         if maxGain == gain:
            print("Splitting attribute is.... %s" % attrib)
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
           #    print("possible values~~~~~~~~~~~~")
               possibleValuesCopy = copy.deepcopy(possibleValues)
               del possibleValuesCopy[attrib]
           #    print(possibleValuesCopy)
           #    print("possible attributes~~~~~~~~~~~~~~~`")
               attribsCopy = copy.deepcopy(attribs)
               attribsCopy.remove(attrib)
            #   print(attribsCopy)
               print("recursive call HERE")
            #   gen_tree(dataCopy, possibleValuesCopy, attribsCopy, classification)

               return

def main():
   parser = lib_lab4.getC45Args()
   parser.parse_args()
   return 0

if __name__ == '__main__':
   rtn = main()
   sys.exit(rtn)
