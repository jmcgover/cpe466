# CPE 466 Fall 2015
# Lab 5: Clustering
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

# Contains the implementation of various utility functions that are primarily
# program and function oriented (as opposed to algorithm related).

import argparse
import os
import sys

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

DESCRIPTION_KMEANS = 'k-Means Clustering'
COL_KMEANS = '90'
def get_k_means_args(description=DESCRIPTION_KMEANS):
   arg_parser = get_arg_parser(description)
   arg_parser.add_argument(
         'csv_filename', metavar='<Filename>',
         help='name of the CSV file containing the input dataset'
         );
   arg_parser.add_argument(
         'k', metavar='<k>', type=int,
         help='number of clusters the program has to produce'
         );
   return arg_parser

DESCRIPTION_HIERARCHICAL = 'Hierarchical Clustering'
COL_HIERARCHICAL = '80'
HELP_HIERARCHICAL= 'R|optional threshold at which your program will "cut" the '
HELP_HIERARCHICAL+='\ncluster hierarchy to report the clusters:'
HELP_HIERARCHICAL+='\n'
HELP_HIERARCHICAL+='\n  If <threshold> parameter IS specified in the input, your'
HELP_HIERARCHICAL+='\n  program shall produce both the cluster hierarchy, and the'
HELP_HIERARCHICAL+='\n  appropriate list of clusters cut at the specified'
HELP_HIERARCHICAL+='\n  threshold.'
HELP_HIERARCHICAL+='\n'
HELP_HIERARCHICAL+='\n  If <threshold> parameter IS NOT specified in the input, your'
HELP_HIERARCHICAL+='\n  program shall produce the cluster hierarchy alone.'
def get_hierarchical_args(description=DESCRIPTION_HIERARCHICAL):
   os.environ['COLUMNS'] = COL_HIERARCHICAL
   arg_parser = get_arg_parser(description)
   arg_parser.add_argument(
         'csv_filename', metavar='<Filename>',
         help='name of the CSV file containing the input dataset'
         );
   arg_parser.add_argument(
         'threshold', metavar='<threshold>', type=float,
         help=HELP_HIERARCHICAL
         );
   return arg_parser
