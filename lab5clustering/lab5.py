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

def get_header_filename(csv_filename):
   basename = os.path.basename(csv_filename)
   filename, extension = os.path.splitext(basename)
   assert extension == '.csv'
   directory = os.path.dirname(csv_filename)
   header_basename = 'header_' + filename + '.txt'
   header_filename = os.path.join(directory, header_basename)
   return header_filename

HELP_HEADER= 'R|name of the CSV file containing the input dataset\'s header'
HELP_HEADER+='\n'
HELP_HEADER+='\n  If [Header_Filename] IS NOT provided, the program can deduce the header'
HELP_HEADER+='\n  file from the data filename by prepending \'header_\' to it, using a'
HELP_HEADER+='\n  \'.txt\' extension instead, and looking in the working directory,'
HELP_HEADER+='\n  by adding the [-i | --infer-header] flag to the arguments.'

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
   arg_parser.add_argument(
         'header_filename', metavar='Header_Filename', default=None, nargs='?',
         help=HELP_HEADER
         );
   arg_parser.add_argument('-i', '--infer-header',
         action='store_true',
         help='infer the header from the data file filename')
   return arg_parser

DESCRIPTION_HIERARCHICAL = 'Hierarchical Clustering'
COL_HIERARCHICAL = '80'
HELP_HTHRESHOLD= 'R|optional threshold at which the program will "cut" the '
HELP_HTHRESHOLD+='\ncluster hierarchy to report the clusters:'
HELP_HTHRESHOLD+='\n'
HELP_HTHRESHOLD+='\n  If <threshold> parameter IS specified in the input, the'
HELP_HTHRESHOLD+='\n  program shall produce both the cluster hierarchy, and the'
HELP_HTHRESHOLD+='\n  appropriate list of clusters cut at the specified'
HELP_HTHRESHOLD+='\n  threshold.'
HELP_HTHRESHOLD+='\n'
HELP_HTHRESHOLD+='\n  If <threshold> parameter IS NOT specified in the input, the'
HELP_HTHRESHOLD+='\n  program shall produce the cluster hierarchy alone.'
def get_hierarchical_args(description=DESCRIPTION_HIERARCHICAL):
   os.environ['COLUMNS'] = COL_HIERARCHICAL
   arg_parser = get_arg_parser(description)
   arg_parser.add_argument(
         'csv_filename', metavar='<Filename>',
         help='name of the CSV file containing the input dataset'
         );
   arg_parser.add_argument(
         'threshold', metavar='threshold', type=float, default=None, nargs='?',
         help=HELP_HTHRESHOLD
         );
   arg_parser.add_argument(
         'header_filename', metavar='Header_Filename', default=None, nargs='?',
         help=HELP_HEADER
         );
   arg_parser.add_argument('-i', '--infer-header',
         action='store_true',
         help='infer the header from the data file filename')
   return arg_parser
