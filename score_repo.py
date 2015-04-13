#!/usr/bin/env python3

import argparse
import sys

def loadAttributePlugins():
  pass

def processConfiguration():
  try:
    pass
  except:
    print("Malformatted or missing configuration.")
    sys.exit(2)

def processArguments():
  parser = argparse.ArgumentParser(description='Calculate the score of a repository.')
  parser.add_argument('integers', metavar='repo_id', type=int, nargs=1, help='Identifier for a repository as it appears in the GHTorrent database.')

  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
  else:
    args = parser.parse_args()
    return args

def main():
  processArguments()
  processConfiguration()
  loadAttributePlugins()

if __name__ == '__main__':
  main()
