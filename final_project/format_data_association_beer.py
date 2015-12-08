#! /usr/local/bin/python3

import errno
import json
import os
import sys

import pymongo
from pymongo import MongoClient

import collections
from collections import defaultdict
from collections import Counter

sys.path.append(os.getcwd())
import untappd
from untappd import BeerDB
from untappd import BeerDBMaker
from untappd import UntappdRequester
from untappd import UntappdDB


def main():
   db = UntappdDB()
   beer_db = BeerDBMaker()
   transactions = defaultdict(list)
   # BUILD TRANSCACTIONS
   for checkin in db.query('checkins'):
      user = checkin['user']['user_name']
      rating = checkin['rating_score']
      brewery = checkin['brewery']['brewery_name']
      beer = checkin['beer']['beer_name']
      id = beer_db.add_beer(brewery, beer)
      transactions[(user, rating)].append(id)
   # SAVE TRANSACTIONS FILE
   with open('out1_untappd.csv', 'w') as transactions_file:
      for (user, rating),beer_list in transactions.items():
         print('%s-%s, %s' % (user, rating, str(beer_list).strip('[').strip(']')), file=transactions_file)
   # SAVE BEER DB
   with open('beers.csv', 'w') as beer_db_file:
      beer_db.print_table(beer_db_file)

   # TEST PARSE
   beers = BeerDB('beers.csv')

   return 0

if __name__ == '__main__':
   rtn = main()
   sys.exit(rtn)
