#! /usr/local/bin/python3

# CPE 466 Fall 2015
# Lab 6: Association Rule Mining
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import errno
import os
import sys

sys.path.append(os.getcwd())
import lab6

import bakery
from bakery import MarketBasketTransactions
from bakery import GoodsDatabase
from bakery import Good

def main():
   # PARSE ARGS
   data_filename = None
   min_sup = None
   min_conf = None
   arg_parser = lab6.get_association_args()
   args = arg_parser.parse_args()
   data_filename = args.csv_filename
   min_sup = args.min_sup
   min_conf = args.min_conf
   # BUILD GOODS DB
   goods_db = GoodsDatabase('goods.csv')
   # BUILD BASKETS
   transactions = MarketBasketTransactions(data_filename)
   for item in transactions.get_items():
      item_set = set()
      item_set.add(item)
      print('Item {0}: {1}'.format(item, transactions.support(item_set)))
   for x in transactions.get_items():
      X = set()
      X.add(x)
      for y in transactions.get_items():
         Y = set()
         Y.add(y)
         transactions.confidence(X,Y)

   return 0

if __name__ == '__main__':
   rtn = main()
   sys.exit(rtn)
