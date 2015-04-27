#!/usr/bin/env python3

import argparse
from core import establish_database_connection
from core import load_attribute_plugins
from core import init_attribute_plugins
from core import process_configuration
from core import process_repository
from core import save_result
import os
import random
import sys
import threading
import time
from utilities import is_dir


def process_arguments():
    """
    Uses the argparse module to parse commandline arguments.

    Returns:
        Dictionary of parsed commandline arguments.
    """
    parser = argparse.ArgumentParser(
        description='Calculate the score of a repository.'
    )
    parser.add_argument(
        '-c',
        '--config',
        type=argparse.FileType('r'),
        default='config.json',
        dest='config_file',
        help='Path to the configuration file.'
    )
    #parser.add_argument(
    #    'repository_ids',
    #    type=int,
    #    nargs='+',
    #    help='List of identifiers for repositories as they appear in the \
    #          GHTorrent database.'
    #)
    parser.add_argument(
        '-p',
        '--fetched-path',
        type=is_dir,
        dest='repository_path',
        #nargs=1,
        help='Path to the repository source code.'
    )
    parser.add_argument(
        '-s',
        '--repos-sample',
        type=argparse.FileType('r'),
        dest='repos_sample',
        help='Path to the sample file'
    )

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()


def main():
    """
    Main execution flow.
    """
    args = process_arguments()
    config = process_configuration(args.config_file)
    connection = establish_database_connection(config['options']['datasource'])
    attributes = config['attributes']
    load_attribute_plugins(attributes)
    init_attribute_plugins(attributes, connection)

    repository_ids = args.repos_sample.read().strip().split('\n')
    for repo_id in repository_ids:
        score, results = process_repository(
            repo_id, 
            args.repository_path + repo_id,
            attributes,
            connection
        )

        print('{}, {}'.format(repo_id, score))

#        if config['options'].get('persistResult', False):
#            save_result(args.repository_id, results, connection.cursor())
#            print('\rResult saved to datasource.')
#            print('\rRaw score: {0}'.format(score))
#        else:
#            print('\rRaw score: {0}'.format(score))

    connection.close()


def spin(stop_condition):
    while not stop_condition:
        print(chr(random.randint(int('2800', 16), int('2880', 16))), end='')
        sys.stdout.flush()
        print('\b', end='')
        time.sleep(0.1)

if __name__ == '__main__':
    stop_condition = False
    spinner_thread = threading.Thread(target=spin, args=([stop_condition]))
    spinner_thread.daemon = True
    spinner_thread.start()
    try:
        main()
    except KeyboardInterrupt:
        print('\rCaught interrupt, exiting.')
    finally:
        stop_condition = True
