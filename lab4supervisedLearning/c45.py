#! /usr/local/bin/python3

# CPE 466 Fall 2015
# Lab 4: Supervised Learning
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import math

def calc_entropy(allDataRows, possibleValues, classification):
   entropy = 0
   total = len(allDataRows[classification])
   for label in possibleValues[classification]:
      count = allDataRows[classification].count(label)
      prob = float(count/total)
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
      prob = float(count/total)
      gain += prob * math.log(prob,2)

   gain += calc_entropy(allDataRows, possibleValues, classification)
   return gain

# TO DO make a recursive driver for this junk

