#!/usr/bin/env python3

import argparse
from core import establish_database_connection
from core import load_attribute_plugins
from core import process_configuration
from core import process_repository
from core import save_result
import os
import sys
import threading
import time
from utilities import is_dir


def repository_path(path_string):
    if os.path.exists(path_string):
        return path_string
    else:
        raise argparse.ArgumentTypeError(
            '{0} is not a directory.'.format(path_string)
        )


def process_arguments():
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
    parser.add_argument(
        'repository_id',
        type=int,
        nargs=1,
        help='Identifier for a project as it appears in the \
              GHTorrent database.'
    )
    parser.add_argument(
        'repository_path',
        type=repository_path,
        nargs=1,
        help='Path to the repository source code.'
    )

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()


def main():
    args = process_arguments()
    config = process_configuration(args.config_file)
    connection = establish_database_connection(config['options']['datasource'])
    attributes = config['attributes']
    load_attribute_plugins(attributes)

    score, results = process_repository(
        args.repository_id[0],
        args.repository_path[0],
        attributes,
        connection
    )

    if config['options'].get('persistResult', False):
        save_result(args.repository_id, results, connection.cursor())
        print('\rResult saved to datasource.')
    else:
        print('\rRaw score: {0}'.format(score))

    connection.close()


def spin(stop_condition):
    tokens = ['-', '\\', '|', '/']
    while not stop_condition:
        for token in tokens:
            sys.stdout.write(token)
            time.sleep(0.1)
            sys.stdout.flush()
            sys.stdout.write('\b')

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
