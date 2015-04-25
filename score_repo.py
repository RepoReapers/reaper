#!/usr/bin/env python3

import argparse
import importlib
import json
import mysql.connector
import os
import sys
import threading
import time
from utilities import is_dir


def save_result(repo_id, results, cursor):
    """
    Save the results to the specified data source.
    """
    return
    # Very much under a TODO
    try:
        query = 'CREATE TABLE {0}'.format(
            'results_' + time.strftime('%Y-%m-%d')
        )
        cursor.execute(query)
    except mysql.connector.Error as error:
        print('test')
    finally:
        query = 'INSERT INTO results () VALUES ()'
        cursor.execute(query)


def process_repo(project_id, repo_path, attributes, connection):
    score = 0
    results = {}
    for attribute in attributes:
        cursor = connection.cursor()

        if 'implementation' in attribute:
            result = attribute['implementation'].run(
                project_id,
                repo_path,
                cursor,
                **attribute['options']
            )

            cursor.close()

            score += int(result or 0) * attribute['weight']
            results[attribute['name']] = result

            if ('essential' in attribute and
                    attribute['essential'] and
                    not result):
                score = 0
                break

    return score, results


def load_attribute_plugins(attributes):
    for attribute in attributes:
        if attribute['enabled']:
            try:
                attribute['implementation'] = importlib.import_module(
                    'attributes.{0}.main'.format(attribute['name'])
                )
            except ImportError:
                print('Failed to load the {0} attribute.'.format(
                        attribute['name']
                    )
                )


def establish_database_connection(config):
    try:
        connection = mysql.connector.connect(**config)
        connection.connect()
        return connection
    except mysql.connector.Error:
        print('\rUnable to establish connection to database.')
        sys.exit(1)


def process_configuration(config_file):
    try:
        config = json.load(config_file)
        if 'options' in config and 'attributes' in config:
            for attribute in config['attributes']:
                if 'name' not in attribute:
                    attribute['enabled'] = False
                if 'enabled' not in attribute:
                    attribute['enabled'] = False
                if 'weight' not in attribute:
                    attribute['weight'] = 5
                if 'options' not in attribute:
                    attribute['options'] = {}
            return config
        else:
            print('Configuration is missing required keys. See the sample \
                configuration provided with the repository contents.')
            sys.exit(2)
    except:
        print('Malformatted or missing configuration.')
        sys.exit(2)


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

    score, results = process_repo(
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
