#! /usr/local/bin/python3

# CPE 466 Fall 2015
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

from __future__ import print_function

from math import floor
from math import sqrt

def length(x):
   sumSquares = 0.0
   for i in x:
      sumSquares += i*i
   return sqrt(sumSquares)

def dot(x, y):
   assert len(x) == len(y)
   dotProduct = 0
   for i,j in zip(x,y):
      dotProduct += i * j
   return dotProduct

def euclidean_distance(x, y):
   assert len(x) == len(y), 'x: %s y: %s' % (x,y)
   sumSquares = 0.0
   for i,j in zip(x, y):
      sumSquares += (i - j) * (i - j)
   return sqrt(sumSquares)

def manhattan_distance(x, y):
   assert len(x) == len(y)
   sumProjections = 0
   for i,j in zip(x, y):
      sumProjections += abs(i - j)
   return sumProjections

def avg(x):
   if len(x) == 0:
      return 0
   return sum(x) / len(x)
def stdev(x):
   if len(x) == 0:
      return 0
   eX = avg(x)
   deviation = 0
   for i in x:
       deviation += (i - eX) * (i - eX)
   return sqrt(deviation/len(x))
def cov(x, y):
   assert len(x) == len(y)
   if len(x) == 0 or len(y) == 0:
      return 0
   eX = avg(x)
   eY = avg(y)
   n = len(x)
   covXY = 0
   for i,j in zip(x,y):
      covXY += ((i - eX) * (j - eY))/n
   return covXY
def pearson_correlation(x, y):
   assert len(x) == len(y)
   if len(x) == 0 or len(y) == 0:
      return 0;
   std_x = stdev(x)
   std_y = stdev(y)
   if std_x == 0 or std_y == 0:
      return 0
   return cov(x,y) / (std_x * std_y)

def mean_row(x):
   return avg(x)
def max_row(x):
   return max(x)
def min_row(x):
   return min(x)
def median_row(x):
   sortedX = sorted(x)
   return sortedX[int(floor(len(x) / 2))]

def get_col(x, ndx):
   column = []
   for i in x:
      column.append(i[ndx])
   return column

def avg_col(x, ndx):
   return avg_row(get_col(x, ndx))

def max_col(x, ndx):
   return max_row(get_col(x, ndx))

def min_col(x, ndx):
   return min_row(get_col(x, ndx))

def median_col(x, ndx):
   column = get_col(x, ndx)
   sorted_col = sorted(column)
   return sorted_col[floor(len(x) / 2)]

def main():
   a = [1,1,1,1,1]
   b = [2,2,2,2,2]
   c = [6,3,4,1,0]
   d = [8,4,6,2,1]
   e = [7,4,5,3,1]
   print('Length %s: %f' % (a, length(a)))
   print('Dot %s and %s: %f' % (a, b, dot(a,b)))
   print('Euc %s and %s: %f' % (a, b, euclidean_distance(a,b)))
   print('Man %s and %s: %f' % (a, b, manhattan_distance(a,b)))
   print('Pea %s and %s: %f' % (a, b, pearson_correlation(a,b)))
   print('Med %s: %d' % (c, median_row(c)))
   print('Med %s: %d' % ([a,b,c,d,e], median_col([a,b,c,d,e], 2)))

if __name__ == '__main__' :
   main()
