#! /usr/bin/python

import sys
import os

# Custom files
sys.path.append(os.getcwd())
from vocabulary import Vocabulary

class Document(object):
    def __init__(self):
        print('Made a new document class!')
