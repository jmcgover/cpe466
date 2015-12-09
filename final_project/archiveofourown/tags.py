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

class TagsDatabase(object):
   def __init__(self, csv_filename):
      # INITIALIZE MEMBERS
      self.csv_filename = csv_filename
      self.tags_db = None
      self.header = None

      # READ FILE
      tags_db = dict()
      header = None
      with open(csv_filename) as tags_db_file:
         header = tags_db_file.__next__()
         for record in tags_db_file:
            tag = Tag(csv_str=record)
            tags_db[tag.id] = tag
      self.tags_db = tags_db
      self.header = header
   def __iter__(self):
      return self.tags_db.items().__iter__()
   def get_tag(self, id):
      return self.tags_db[id]
   def get_name(self, id):
      return self.tags_db[id].name
   def get_type(self, id):
      return self.tags_db[id].type
   def get_count(self, id):
      return self.tags_db[id].count

   def id_str(self, id):
      return '(%s)' % (self.tags_db[id].name)

class Tag(object):
   def __init__(self,
         id=None,
         name=None,
         type=None,
         count=None,
         csv_str=None,
         tuple=None):
      # INITIALIZE MEMBERS
      self.id = None
      self.name = None
      self.type = None
      self.count = None

      # PARSE DATA
      if csv_str:
         tuple = csv_str.split(',')
         assert len(tuple) == 4 , 'invalid csv:incorrect number of elements:'\
               + '%d(must be 4)' % len(tuple)
      if tuple:
         assert len(tuple) == 4 ,\
            'invalid tuple:incorrect length:%d(must be 4)' % len(tuple)
         id = int(tuple[0])
         name = tuple[1]
         type = tuple[2]
         count = float(tuple[3])
      if not csv_str and not tuple:
         assert id     != None
         assert name != None
         assert type   != None
         assert count  != None

      self.id = id
      self.name = name
      self.type = type
      self.count = count
   def __hash__(self):
      return self.id.__hash__()

def main():
   goods_db = TagsDatabase('alltags.csv')
   print(type(tags_db.tags_db))
   print(tags_db.tags_db)
   for id,tag in tags_db:
      print(id,tag)
      print(tags_db.get_tag(id))
      print('{0:>5}:{1}'.format('id', good.id))
      print('{0:>5}:{1}'.format('name', good.name))
      print('{0:>5}:{1}'.format('type', good.type))
      print('{0:>5}:{1}'.format('count', good.count))

   return 0

if __name__ == '__main__':
   rtn = main()
   sys.exit(rtn)
