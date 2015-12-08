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
from untappd import UntappdRequester
from untappd import UntappdDB

def main():
   db = UntappdDB()
   cursor = db.query('user_feeds')
   client_id='A346C811ED9267F004471FF258E67A219D399BCB'
   client_secret='320CF0D911C7256FA58DC973CFDF91CBF5689F74'
   lat = 35.278222
   long = -120.666552
   requester = UntappdRequester(client_id, client_secret, 50)
   #requester.get_all_pub_activity(lat, long, 'pub_spikes')
   collected_users = set()
   for cur in db.query('user_feeds'):
      for item in cur['response']['checkins']['items']:
         collected_users.add(item['user']['user_name'])
         #print('USER: %s' % (item['user']['user_name']))
   pub_users = set()
   for cur in db.query('pub_spikes'):
      for item in cur['response']['checkins']['items']:
         pub_users.add(item['user']['user_name'])
         #print('USER: %s' % (item['user']['user_name']))
   for user in pub_users:
      print('PUB USER: %s' % (user))
   for user in collected_users:
      print('COLLECTED USER: %s' % (user))
   uncollected_users = pub_users - collected_users
   for user in uncollected_users:
      print('UNCOLLECTED USER: %s' % (user))
   print('NUM PUB USERS: %d' % (len(pub_users)))
   print('NUM COL USERS: %d' % (len(collected_users)))
   print('NUM UNC USERS: %d' % (len(uncollected_users)))
   return 0

if __name__ == '__main__':
   rtn = main()
   sys.exit(rtn)
