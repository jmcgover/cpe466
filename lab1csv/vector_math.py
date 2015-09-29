#! /usr/bin/python
from __future__ import print_function

from math import floor
from math import sqrt

def length(x):
    sumSquares = 0.0
    for i in x:
        sumSquares += i*i
    return sqrt(sumSquares)

def dot(x, y):
    if len(x) != len(y):
        raise ArithmeticError('vectors must have identical length')

    dotProduct = 0
    for i,j in zip(x,y):
        dotProduct += i * j
    return dotProduct

def euclideanDistance(x, y):
    if len(x) != len(y):
        raise ArithmeticError('vectors must have identical length')

    sumSquares = 0.0
    for i,j in zip(x, y):
        sumSquares += i * j
    return sqrt(sumSquares)

def manhattanDistance(x, y):
    if len(x) != len(y):
        raise ArithmeticError('vectors must have identical length')

    sumProjections = 0
    for i,j in zip(x, y):
        sumProjections += abs(i - j)
    return sumProjections

def avg(x):
    return sum(x) / len(x)
def stdev(x):
    eX = avg(x)
    deviation = 0
    for i in x:
        deviation += (i - eX) * (i - eX)
    return sqrt(deviation/len(x))
def pearsonCorrelation(x, y):
    if len(x) != len(y):
        raise ArithmeticError('vectors must have identical length')

    covXY = 0
    eX = avg(x)
    eY = avg(y)
    stdevX = stdev(x)
    stdevY = stdev(y)
    if len(x) > 0 and stdevX > 0 and stdevY > 0:
        for i,j in zip(x,y):
            covXY += (i - eX) * (j - eY)
        return (covXY) / ((len(x) - 1) * stdev(x) * stdev(y))
    else:
        return 0.0

def avgRow(x):
    return avg(x)
def maxRow(x):
    return max(x)
def minRow(x):
    return min(x)
def medianRow(x):
    sortedX = sorted(x)
    return sortedX[floor(len(x) / 2)]







def getCol(x, ndx):
    column = []
    for i in x:
        column.append(i[ndx])
    return column

def avgCol(x, ndx):
    return avgRow(getCol(x, ndx))

def maxCol(x, ndx):
    return maxRow(getCol(x, ndx))

def minCol(x, ndx):
    return minRow(getCol(x, ndx))

def medianCol(x, ndx):
    column = getCol(x, ndx)
    sortedCol = sorted(column)
    return sortedCol[floor(len(x) / 2)]

def main():
    a = [1,1,1,1,1]
    b = [2,2,2,2,2]
    c = [6,3,4,1,0]
    d = [8,4,6,2,1]
    e = [7,4,5,3,1]
    print('Length %s: %f' % (a, length(a)))
    print('Dot %s and %s: %f' % (a, b, dot(a,b)))
    print('Euc %s and %s: %f' % (a, b, euclideanDistance(a,b)))
    print('Man %s and %s: %f' % (a, b, manhattanDistance(a,b)))
    print('Pea %s and %s: %f' % (a, b, pearsonCorrelation(a,b)))
    print('Med %s: %d' % (c, medianRow(c)))
    print('Med %s: %d' % ([a,b,c,d,e], medianCol([a,b,c,d,e], 2)))


if __name__ == '__main__' :
    main()
