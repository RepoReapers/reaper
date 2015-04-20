#!/usr/bin/env python3

import argparse
import importlib
import json
import mysql.connector
import os
import sys


def save_result(repo_id, results):
    pass


def load_attribute_plugins(attributes):
    for attribute in attributes:
        if attribute['enabled']:
            try:
                attribute['implementation'] = importlib.import_module(
                    "attributes.{0}.main".format(attribute['name'])
                )
            except ImportError:
                print("Failed to load the {0} attribute.".format(
                        attribute['name']
                    )
                )


def establish_database_connection(config):
    try:
        connection = mysql.connector.connect(**config)
        return connection
    except mysql.connector.Error:
        print("Unable to establish connection to database.")
        sys.exit(1)


def process_configuration(config_file):
    try:
        # TODO: Validate configuration contents
        config = json.load(config_file)
        return config
    except:
        print("Malformatted or missing configuration.")
        sys.exit(2)


def repository_path(path_string):
    if os.path.exists(path_string):
        return path_string
    else:
        raise argparse.ArgumentTypeError(
            "{0} is not a directory.".format(path_string)
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
        dest='config_file', help='Path to the configuration file.'
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

    if len(sys.argv) is 1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()


def main():
    args = process_arguments()
    config = process_configuration(args.config_file)
    connection = establish_database_connection(config['options']['datasource'])
    attributes = config['attributes']
    load_attribute_plugins(attributes)

    score = 0
    results = {}
    for attribute in attributes:
        cursor = connection.cursor()

        if 'implementation' in attribute:
            result = attribute['implementation'].run(
                args.repository_id[0],
                args.repository_path[0],
                cursor,
                **attribute['options']
            )

        score += int(result or 0) * attribute['weight']
        results[attribute['name']] = result

        if 'essential' in attribute and attribute['essential'] and not result:
            score = 0
            break

    if config['options'].get('persistResult', False):
        save_result(args.repository_id, results)
    else:
        print("Raw score: {0}".format(score))

    connection.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Caught interrupt, exiting.")
        sys.exit(1)
