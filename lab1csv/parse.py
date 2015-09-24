#!/usr/bin/python
import sys
import os

def main():
    print 'hello'

    # Initial input checking
    if len(sys.argv) < 2:
        print("Insufficient arguments. Usage: parse.py <fileName>")
        sys.exit()
    if os.path.isfile(sys.argv[1]) == False:
        print("File does not exist.")
        sys.exit()
    return 0

if __name__ == '__main__':
    main()
