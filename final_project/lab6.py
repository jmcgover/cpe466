#! /usr/local/bin/python3

# CPE 466 Fall 2015
# Lab 6: Association Rule Mining
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

# Contains the implementation of various utility functions that are primarily
# program and function oriented (as opposed to algorithm related).

import argparse
import os
import sys

sys.path.append(os.getcwd())

# ARGUMENTS
class SmartFormatter(argparse.HelpFormatter):

    def _split_lines(self, text, width):
        # this is the RawTextHelpFormatter._split_lines
        if text.startswith('R|'):
            return text[2:].splitlines()
        return argparse.HelpFormatter._split_lines(self, text, width)
def get_arg_parser(description):
   return argparse.ArgumentParser(prog=sys.argv[0],
         description=description,
         formatter_class=SmartFormatter
         )

def restricted_float(x):
    x = float(x)
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]"%(x,))
    return x

DESCRIPTION_ASSOCIATION = 'Association Rule Mining'
COL_ASSOCIATION = '90'
def get_association_args(description=DESCRIPTION_ASSOCIATION):
   arg_parser = get_arg_parser(description)
   arg_parser.add_argument(
         'csv_filename', metavar='filename',
         help='name of the CSV file containing the input dataset'
         );
   arg_parser.add_argument(
         'min_sup', metavar='<min_sup>', type=restricted_float,
         help='minimum support number for frequent itemset and association rule discovery'
         );
   arg_parser.add_argument(
         'min_conf', metavar='<min_conf>', type=restricted_float,
         help='minimum confidence number for association rule discovery.'
         );
   return arg_parser
