#!/usr/bin/env python3

import argparse
import os
from score_repo import load_attribute_plugins
from score_repo import establish_database_connection
from score_repo import process_configuration
from score_repo import process_repo
import sys
from utilities import is_dir


def process_arguments():
    parser = argparse.ArgumentParser(
        description='Calculate the scores of a set of repositories.'
    )
    parser.add_argument(
        '-c',
        '--config',
        type=argparse.FileType('r'),
        default='config.json',
        dest='config_file',
        help='Path to the configuration file.'
    )
    parser.add_argument(
        'repositories_path',
        type=is_dir,
        nargs=1,
        help='Path to the repositories.'
    )

    if len(sys.argv) < 1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()


def main():
    args = process_arguments()
    config = process_configuration(args.config_file)
    connection = establish_database_connection(config['options']['datasource'])
    attributes = config['attributes']
    load_attribute_plugins(attributes)

    repos_root = args.repositories_path[0]
    repositories = os.listdir(repos_root)

    for repository_id in repositories:
        score, result = process_repo(
            args.repositories_path[0],
            '{0}/{1}/repo'.format(repos_root, repository_id),
            attributes,
            connection
        )

        if score > config['thresold']:
            result_char = '\033[92m✓\033[0m'
        else:
            result_char = '\033[91m✘\033[0m'

        print('{0}:\t{1} ({2})'.format(repository_id, score, result_char))

if __name__ == '__main__':
    main()