# CPE 466 Fall 2015

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

DESCRIPTION_UNTAPPD = 'Untappd Retrival Library'
COL_UNTAPPD = '90'
def get_association_args(description=DESCRIPTION_UNTAPPD):
   arg_parser = get_arg_parser(description)
   arg_parser.add_argument(
         '-u', '--username' metavar='filename',
         help='name of the CSV file containing the input dataset'
         );
   return arg_parser

