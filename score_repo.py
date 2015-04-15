#!/usr/bin/env python3

import argparse
import importlib
import json
import os
import sys

def load_attribute_plugins(attributes):
    for attribute in attributes:
        if attribute['enabled']:
            try:
                attribute['implementation'] = importlib.import_module("attributes.{0}.main".format(attribute['name']))
            except ImportError:
                print("Failed to load the {0} attribute.".format(attribute['name']))

def process_configuration(config_file):
    try:
        config = json.load(config_file)
        return config
    except:
        print("Malformatted or missing configuration.")
        sys.exit(2)

def repository_path(path_string):
    if os.path.exists(path_string):
        if os.path.exists("{0}/.git".format(path_string)):
            return path_string
        else:
            raise argparse.ArgumentTypeError("{0} is not a git repository.".format(path_string))
    else:
        raise argparse.ArgumentTypeError("{0} is not a directory.".format(path_string))

def process_arguments():
    parser = argparse.ArgumentParser(description='Calculate the score of a repository.')
    parser.add_argument('-c', '--config', type=argparse.FileType('r'), default='config.json', dest='config_file', help='Path to the configuration file.')
    parser.add_argument('repository_id', type=int, nargs=1, help='Identifier for a repository as it appears in the GHTorrent database.')
    parser.add_argument('repository_path', type=repository_path, nargs=1, help='Path to the repository source code.')

    if len(sys.argv) is 1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()

def main():
    args = process_arguments()
    config = process_configuration(args.config_file)
    attributes = config['attributes']
    load_attribute_plugins(attributes)

    score = 0
    for attribute in attributes:
        result = attribute['implementation'].run(config.repository_id, config.repository_path, attribute['options'])
        score += result * attribute['weight']

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Caught interrupt, exiting.")
        sys.exit(1)
