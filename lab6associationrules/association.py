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

import itertools
from itertools import combinations

sys.path.append(os.getcwd())
import lab6

import bakery
from bakery import GoodsDatabase
from bakery import Good

class Candidate(object):
   def __init__(self, items):
      self.frozen = frozenset(items) # The association of sets
      self.items = set(items) # Set of all items in candidate

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
   def get_get_transactions(self):
      return self.baskets
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

class Apriori(object):
   def __self__():
      return
   def get_associations(self, T, min_sup, min_conf, skyline=False):
      print('Generating frequent itemsets for %.3f...' % (min_sup), file=sys.stderr)
      frequent = self.apriori(T, min_sup)
      print('Generating rules with confidence %.3f...' % (min_conf), file=sys.stderr)
      rules = self.gen_rules(T, frequent, min_conf)
      print('DONE', file=sys.stderr)
      return frequent, rules
   def gen_rules(self, T, F, min_conf):
      rules = set()
      H = [None, None]
      for k in range(2, len(F)):
         for f in F[k]:
            H[1] = []
            for s in f:
               antecedent = f - {s}
               consequent = {s}
               if T.confidence(antecedent, consequent) >= min_conf:
                  rules.add((frozenset(antecedent), frozenset(consequent)))
                  H[1].append(consequent)
               #else:
                  #print('skipping %s-->%s' % (antecedent, consequent), file-sys.stderr)
            self.ap_gen_rules(T, f, min_conf, rules, H, k, 1)
      return rules
   def ap_gen_rules(self, T, f, min_conf, rules, H, k, m):
      if k > m + 1 and H[m]:
         H.append(None)
         H[m + 1] = self.candidate_gen(H, m)
         for h in H[m + 1]:
            confidence = T.confidence(f, f - h)
            if confidence >= min_conf:
               rules.add((frozenset(f - h), frozenset(h)))
         self.ap_gen_rules(T, f, min_conf, rules, H, k, m + 1)
      return
   def candidate_gen(self, F, k):
      C_k = []
      print('\tGenerating Candidates for F[%d]: %s' % (k, F[k]), file=sys.stderr)
      for f_1,f_2 in itertools.combinations(F[k], 2):
         #print('f1: %s f2: %s union: %s' % (f_1, f_2, f_1 | f_2), file=sys.stderr)
         if len(f_1 | f_2) == len(f_1) + 1:
            c = f_1 | f_2
            add_candidate = True
            #print('c %d: %s' % (k, c), file=sys.stderr)
            for s in combinations(c,k):
               subset = set(s)
               #print('subset: %s' % (subset), file=sys.stderr)
               if subset not in F[k]:
                  add_candidate = False
               #else:
                  #print('skipping: %s' % (subset), file=sys.stderr)
            C_k.append(c) if add_candidate else None
      return C_k
   def apriori(self, T, min_sup):
      C = [None, None] # Candidates
      C[1] = [{c} for c in T.get_items()]
      F = [None, None] # Frequent Itemsets
      F[1] = [f for f in C[1] if T.support(f) >= min_sup]
      k = 2
      while len(F[k - 1])  > 0:
         #print('k: %d | F[%d]: %s' % (k, k - 1, F[k - 1]), file=sys.stderr)
         C.append(None) #C_k
         C[k] = self.candidate_gen(F, k-1)
         #print('C[%d]: %s' % (k,C[k]), file=sys.stderr)
         F.append([])
         for c in C[k]:
            support = T.support(c)
            if T.support(c) >= min_sup and c not in F[k]:
               F[k].append(c)
         k += 1
         #print('len(F[%d-1]): %d' % (k, len(F[k - 1])), file=sys.stderr)
      del F[k-1] # Gets rid of the empty list
      return F
   def get_id_str(self, itemset, db):
      str = None
      for id in itemset:
         if str:
            str += '-' + db.id_str(id)
         else:
            str = db.id_str(id)
      return str
   def get_row_tuple(self, T, rule, db):
      antecedent_str, consequent_str, support, confidence = None, None, None, None
      if not rule:
         return
      a,c = rule
      antecedent_str = self.get_id_str(a, db)
      consequent_str = self.get_id_str(c, db)
      support = T.support(a | c)
      confidence = T.confidence(a , c)
      return support, confidence, antecedent_str, consequent_str
   def print_items_csv(self, T, db, frequent, file=sys.stdout):
      print('%s,%s,%s,%s' % \
            ('size', 'itemset', 'support', ''), file=file)
      for f,k in zip(frequent, range(len(frequent))):
         if f:
            for e in f:
               print('%s,%s,%s,%s' % (k, T.support(e), self.get_id_str(e, db),''), file=file)
   def print_rules_csv(self, T, db, rules, file=sys.stdout):
      print('%s,%s,%s,%s' % \
            ('support', 'confidence', 'antecedent', 'consequent'), file=file)
      for rule in rules:
         print('%.3f,%.3f,%s,%s' % self.get_row_tuple(T, rule, db), file=file)

   def print_items_latex(self, T, db, frequent, file=sys.stdout):
      print('%s,%s,%s,%s' % \
            ('size', 'itemset', 'support', ''), file=file)
      for f,k in zip(frequent, range(len(frequent))):
         if f:
            for e in f:
               print('%s,%s,%s,%s' % (k, T.support(e), self.get_id_str(e, db),''), file=file)
   def print_rules_latex(self, T, db, rules, file=sys.stdout):
      print('%s,%s,%s,%s' % \
            ('support', 'confidence', 'antecedent', 'consequent'), file=file)
      for rule in rules:
         print('%.3f,%.3f,%s,%s' % self.get_row_tuple(T, rule, db), file=file)


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
   # CALC ASSOCIATIONS
   apriori = Apriori()
   frequent, rules = apriori.get_associations(transactions, min_sup, min_conf)
   outfile = sys.stdout
   print('%s,%s,%s,%s' % ('file','min_sup','min_conf',''), file=outfile)
   print('%s,%s,%s,%s' % (data_filename,min_sup,min_conf,''), file=outfile)
   apriori.print_items_csv(transactions, goods_db, frequent)
   apriori.print_rules_csv(transactions, goods_db, rules)
   return 0

if __name__ == '__main__':
   rtn = main()
   sys.exit(rtn)
