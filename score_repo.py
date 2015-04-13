#!/usr/bin/env python3

import argparse
import importlib
import json
import sys

def loadAttributePlugins(attributes):
  for attribute in attributes:
    try:
      attribute['implementation'] = importlib.import_module("attributes.{0}.main".format(attribute['name']))
    except ImportError:
      print("Failed to load the {0} attribute.".format(attribute['name']))

def processConfiguration(config_file):
  try:
    config = json.load(config_file)
    return config
  except:
    print("Malformatted or missing configuration.")
    sys.exit(2)

def processArguments():
  parser = argparse.ArgumentParser(description='Calculate the score of a repository.')
  parser.add_argument('-c', '--config', type=argparse.FileType('r'), default='config.json', dest='config_file', help='Path to the configuration file.')
  parser.add_argument('repository_id', type=int, nargs=1, help='Identifier for a repository as it appears in the GHTorrent database.')

  if len(sys.argv) is 1:
    parser.print_help()
    sys.exit(1)

  return parser.parse_args()

def main():
  args = processArguments()
  config = processConfiguration(args.config_file)
  attributes = config['attributes']
  loadAttributePlugins(attributes)

  score = 0
  for attribute in attributes:
    result = attribute['implementation'].run(metadata, repo_path, attribute['options'])
    score += result * attribute['weight']

if __name__ == '__main__':
  main()
