#! /usr/local/bin/python3

import errno
import json
import os
import sys

import urllib
from urllib import parse
from urllib import request

import urllib
from pymongo import MongoClient

class TypeDBMaker(object):
   def __init__(self):
      self.type_db = {}
      self.next_id = 1
   def add_beer(self,type_name):
      if (brewery, name) not in self.type_db:
         self.type_db[type_name] = self.next_id
         self.next_id += 1
      return self.type_db[type_name]
   def get_beer_id(self, type_name):
      return self.type_db[type_name]
   def print_table(self, file=sys.stdout):
      print('%s, %s' % ('id', 'type'), file=file)
      for type,id in self.type_db.items():
         print('%d, %s' % (id, type.replace(',',' '))

class BeerDB(object):
   def __init__(self, csv_filename):
      # INITIALIZE MEMBERS
      self.csv_filename = csv_filename
      self.type_db = None
      self.header = None

      # READ FILE
      type_db = dict()
      header = None
      with open(csv_filename) as type_db_file:
         header = type_db_file.__next__()
         for record in type_db_file:
            new_type = Type(csv_str=record)
            type_db[new_type.id] = new_type
      self.type_db = type_db
      self.header = header
   def __iter__(self):
      return self.type_db.items().__iter__()
   def get_type_name(self, id):
      return self.type_db[id].type
   def get_type_str(self, id):
      type = self.get_type_name(id)
      return '(%s)' % (type.strip())
   def id_str(self, id):
      return self.get_type_str(id)

class Type(object):
   def __init__(self,
         id=None,
         type=None,
         csv_str=None,
         tuple=None):
      # INITIALIZE MEMBERS
      self.id = None
      self.type = None

      # PARSE DATA
      if csv_str:
         tuple = csv_str.split(',')
         assert len(tuple) == 2 , 'invalid csv:incorrect number of elements:'\
               + '%d(must be 2)' % len(tuple)
      if tuple:
         assert len(tuple) == 2 ,\
            'invalid tuple:incorrect length:%d(must be 2)' % len(tuple)
         id = int(tuple[0])
         type = tuple[1]
      if not csv_str and not tuple:
         assert id     != None
         assert type != None

      self.id = id
      self.type = type
   def __hash__(self):
      return self.id.__hash__()

class BeerDBMaker(object):
   def __init__(self):
      self.beer_db = {}
      self.next_id = 1
   def add_beer(self,brewery,name):
      if (brewery, name) not in self.beer_db:
         self.beer_db[(brewery, name)] = self.next_id
         self.next_id += 1
      return self.beer_db[(brewery, name)]
   def get_beer_id(self, brewery, name):
      return self.beer_db[(brewery, name)]
   def print_table(self, file=sys.stdout):
      print('%s, %s, %s' % ('id', 'brewery', 'beer'), file=file)
      for (brewery, beer),id in self.beer_db.items():
         print('%d, %s, %s' % (id, brewery.replace(',',''), beer.replace(',','_')), file=file)


class Beer(object):
   def __init__(self,
         id=None,
         brewery=None,
         beer=None,
         csv_str=None,
         tuple=None):
      # INITIALIZE MEMBERS
      self.id = None
      self.brewery = None
      self.beer = None

      # PARSE DATA
      if csv_str:
         tuple = csv_str.split(',')
         assert len(tuple) == 3 , 'invalid csv:incorrect number of elements:'\
               + '%d(must be 3)' % len(tuple)
      if tuple:
         assert len(tuple) == 3 ,\
            'invalid tuple:incorrect length:%d(must be 3)' % len(tuple)
         id = int(tuple[0])
         brewery = tuple[1]
         beer = tuple[2]
      if not csv_str and not tuple:
         assert id     != None
         assert brewery != None
         assert beer   != None

      self.id = id
      self.brewery = brewery
      self.beer = beer
   def __hash__(self):
      return self.id.__hash__()

class BeerDB(object):
   def __init__(self, csv_filename):
      # INITIALIZE MEMBERS
      self.csv_filename = csv_filename
      self.beer_db = None
      self.header = None

      # READ FILE
      beer_db = dict()
      header = None
      with open(csv_filename) as beer_db_file:
         header = beer_db_file.__next__()
         for record in beer_db_file:
            good = Beer(csv_str=record)
            beer_db[good.id] = good
      self.beer_db = beer_db
      self.header = header
   def __iter__(self):
      return self.beer_db.items().__iter__()
   def get_brewery_beer_tuple(self, id):
      return self.beer_db[id].brewery, self.beer_db[id].beer
   def get_brewery_beer_str(self, id):
      brewery,beer = self.get_brewery_beer_tuple(id)
      return '%s+%s' % (brewery.strip(), beer.strip())
   def id_str(self, id):
      return self.get_brewery_beer_str(id)


class UntappdDB(object):
   def __init__(self):
      # Initialize Members
      self.client = None
      self.db = None

      # Open database
      client = MongoClient('localhost', 27017)
      db = client['untappd']

      # Assign Members
      self.client = client
      self.db = db
      return

   def insert_document(self, collection_name, document):
      inserted_id = None
      collection = self.db[collection_name]
      inserted_id = collection.insert_one(document).inserted_id
      return inserted_id
   def query(self, collection_name, query=None, projection=None):
      collection = self.db[collection_name]
      return collection.find(query, projection)


class UntappdRequester(object):
   def __init__(self, client_id, client_secret, request_limit):
      self.api_url = 'https://api.untappd.com/v4/'
      self.client_id = client_id
      self.client_secret = client_secret
      self.request_limit = request_limit
      self.num_requests = 0
      self.db = UntappdDB()
      return
   def get_user_info(self, username, ):
      json_doc = None

      # Define Method Params
      data = {}
      data['client_id'] = self.client_id
      data['client_secret'] = self.client_secret
      method_name = 'user/checkins/%s' % (username)
      if max_id:
         data['max_id'] = max_id
      if min_id:
         data['min_id'] = min_id
      if limit:
         data['limit'] = limit

      # Build URL
      url_values = urllib.parse.urlencode(data)
      request_url = self.api_url + method_name + '?' + url_values
   def get_all_user_activity(self, username):
      prev_min_id = None
      cur_min_id = None
      user_feed = self.get_user_activity_feed(username)
      checkin_ids = []
      for checkin in user_feed['response']['checkins']['items']:
         print(checkin['checkin_id'])
         checkin_ids.append(checkin['checkin_id'])
      cur_min_id = min(checkin_ids)
      while prev_min_id == None or cur_min_id < prev_min_id:
         prev_min_id = cur_min_id
         user_feed = self.get_user_activity_feed(username, max_id = prev_min_id)
         checkin_ids = []
         for checkin in user_feed['response']['checkins']['items']:
            print(checkin['checkin_id'])
            checkin_ids.append(checkin['checkin_id'])
         if len(checkin_ids) == 0:
            break
         cur_min_id = min(checkin_ids)
         print('CUR MIN CHECKIN ID: %d' % cur_min_id)
      print('CUR_MIN: %d PREV_MIN: %d' % (cur_min_id, prev_min_id))
      return
   def get_user_activity_feed(self, username, max_id=None, min_id=None, limit=50):
      json_doc = None

      # Define Method Params
      data = {}
      data['client_id'] = self.client_id
      data['client_secret'] = self.client_secret
      method_name = 'user/checkins/%s' % (username)
      if max_id:
         data['max_id'] = max_id
      if min_id:
         data['min_id'] = min_id
      if limit:
         data['limit'] = limit

      # Build URL
      url_values = urllib.parse.urlencode(data)
      request_url = self.api_url + method_name + '?' + url_values
      print('REQUEST_URL: %s' % (request_url))

      # GET feed data
      self.num_requests += 1
      response = urllib.request.urlopen(request_url).read()
      response_str = response.decode('utf-8')
      json_doc = json.loads(response_str)
      self.db.insert_document('user_feeds', json_doc)
      return json_doc
   def get_all_pub_activity(self, lat, long, collection_name='pub_feed'):
      print('PUB ACTIVITY')
      prev_min_id = None
      cur_min_id = None
      pub_feed = self.get_pub_activity(lat, long, collection_name=collection_name)
      checkin_ids = []
      for checkin in pub_feed['response']['checkins']['items']:
         print(checkin['checkin_id'])
         checkin_ids.append(checkin['checkin_id'])
      cur_min_id = min(checkin_ids)
      while prev_min_id == None or cur_min_id < prev_min_id:
         prev_min_id = cur_min_id
         if self.num_requests > self.request_limit:
            return
         pub_feed = self.get_pub_activity(lat, long, max_id = prev_min_id, collection_name=collection_name)
         checkin_ids = []
         for checkin in pub_feed['response']['checkins']['items']:
            print('%s: %d' % (username, checkin['checkin_id']))
            checkin_ids.append(checkin['checkin_id'])
         if len(checkin_ids) == 0:
            break
         cur_min_id = min(checkin_ids)
         print('CUR MIN CHECKIN ID: %d' % cur_min_id)
      print('CUR_MIN: %d PREV_MIN: %d' % (cur_min_id, prev_min_id))
      return
   def get_pub_activity(self, lat, long, max_id=None, min_id=None, limit=None, radius=None, dist_pref='m', collection_name='pub_feed'):
      json_doc = None
      # Define Method Params
      data = {}
      data['client_id'] = self.client_id
      data['client_secret'] = self.client_secret
      method_name = 'thepub/local'
      data['lat'] = lat
      data['lng'] = long
      if max_id:
         data['max_id'] = max_id
      if min_id:
         data['min_id'] = min_id
      if limit:
         data['limit'] = limit
      if radius:
         data['radius'] = radius
      if dist_pref:
         data['dist_pref'] = dist_pref

      # Build URL
      url_values = urllib.parse.urlencode(data)
      request_url = self.api_url + method_name + '?' + url_values

      # GET feed data
      self.num_requests += 1
      response = urllib.request.urlopen(request_url).read()
      response_str = response.decode('utf-8')
      json_doc = json.loads(response_str)
      self.db.insert_document(collection_name, json_doc)
      return json_doc

def main():
   username = sys.argv[1]
   #lat = float(sys.argv[2])
   #long = float(sys.argv[3])
   client_id='A346C811ED9267F004471FF258E67A219D399BCB'
   client_secret='320CF0D911C7256FA58DC973CFDF91CBF5689F74'
   requester = UntappdRequester(client_id, client_secret, 50)
   requester.get_all_user_activity(username)
   #requester.get_all_pub_activity(lat, long, 50, 'pub_spikes')

   return 0

if __name__ == '__main__':
   rtn = main()
   sys.exit(rtn)
