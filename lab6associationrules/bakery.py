#! /usr/local/bin/python3

# CPE 466 Fall 2015
# Lab 6: Association Rule Mining
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import csv
import errno
import os
import sys

import collections
from collections import defaultdict

class GoodsDatabase(object):
   def __init__(self, csv_filename):
      # INITIALIZE MEMBERS
      self.csv_filename = csv_filename
      self.goods_db = None
      self.header = None

      # READ FILE
      goods_db = dict()
      header = None
      with open(csv_filename) as goods_db_file:
         header = goods_db_file.__next__()
         for record in goods_db_file:
            good = Good(csv_str=record)
            goods_db[good.id] = good
      self.goods_db = goods_db
      self.header = header
   def __iter__(self):
      return self.goods_db.items().__iter__()
   def get_good(self, id):
      return self.goods_db[id]
   def get_flavor(self, id):
      return self.goods_db[id].flavor
   def get_food(self, id):
      return self.goods_db[id].food
   def get_price(self, id):
      return self.goods_db[id].price
   def get_type(self, id):
      return self.goods_db[id].type

   def get_flavor_food(self, id):
      return self.goods_db[id].flavor, self.goods_db[id].food
   def get_food_flavor(self, id):
      return self.goods_db[id].food, self.goods_db[id].flavor

class Good(object):
   def __init__(self,
         id=None,
         flavor=None,
         food=None,
         price=None,
         type=None,
         csv_str=None,
         tuple=None):
      # INITIALIZE MEMBERS
      self.id = None
      self.flavor = None
      self.food = None
      self.price = None
      self.type = None

      # PARSE DATA
      if csv_str:
         tuple = csv_str.split(',')
         assert len(tuple) == 5 , 'invalid csv:incorrect number of elements:'\
               + '%d(must be 5)' % len(tuple)
      if tuple:
         assert len(tuple) == 5 ,\
            'invalid tuple:incorrect length:%d(must be 5)' % len(tuple)
         id = int(tuple[0])
         flavor = tuple[1]
         food = tuple[2]
         price = float(tuple[3])
         type = tuple[4]
      if not csv_str and not tuple:
         assert id     != None
         assert flavor != None
         assert food   != None
         assert price  != None
         assert type   != None

      self.id = id
      self.flavor = flavor
      self.food = food
      self.price = price
      self.type = type
   def __hash__(self):
      return self.id.__hash__()

def main():
   goods_db = GoodsDatabase('goods.csv')
   print(type(goods_db.goods_db))
   print(goods_db.goods_db)
   for id,good in goods_db:
      print(id,good)
      print(goods_db.get_good(id))
      print('{0:>6}:{1}'.format('id', good.id))
      print('{0:>6}:{1}'.format('flavor', good.flavor))
      print('{0:>6}:{1}'.format('food', good.food))
      print('{0:>6}:{1}'.format('price', good.price))
      print('{0:>6}:{1}'.format('type', good.type))

   return 0

if __name__ == '__main__':
   rtn = main()
   sys.exit(rtn)
