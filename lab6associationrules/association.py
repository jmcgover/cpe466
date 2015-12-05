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
from bakery import GoodsDatabase
from bakery import Good

class MarketBasketTransactions(object):
   def __init__(self, csv_filename):
      self.baskets = None
      self.num_transactions = None
      self.item_counts = None

      # PARSE BASKETS
      baskets = {}
      item_counts = defaultdict(int)
      with open(csv_filename) as transactions_file:
         csv_reader = csv.reader(transactions_file, delimiter=',')
         # for each transaction
         for record in csv_reader:
            data = [int(e) for e in record] # convert str to int
            # Add transaction to dataset as set of item ids
            baskets[data[0]] = set(data[1:])
            # Increment number of transactions each item shows up in
            for item in baskets[data[0]]:
               item_counts[item] += 1
      self.baskets = baskets
      self.num_transactions = len(baskets)
      self.item_counts = item_counts
   def get_items(self):
      return self.item_counts.keys()
   def get_num_transactions(self):
      return self.num_transactions
   def count(self, X):
      count = 0
      for id,transaction in self.baskets.items():
         if X.issubset(transaction):
            count += 1
      return count
   def support(self, X):
      support_count = self.count(X)
      return support_count / self.num_transactions
   def confidence(self, X, Y):
      return self.count(X.union(Y)) / self.count(X)

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
   return 0

if __name__ == '__main__':
   rtn = main()
   sys.exit(rtn)
