#!/usr/bin/env python3

import argparse
import copy
import json
import multiprocessing
import numbers
import os
import sys
import time
import traceback

from lib.core import load_attribute_plugins
from lib.core import global_init_attribute_plugins
from lib.core import init_attribute_plugins
from lib.core import establish_database_connection
from lib.core import process_configuration
from lib.core import process_plugins
from lib.core import process_key_string
from lib.core import process_repository
from lib.core import get_persist_attrs
from lib.core import get_run_id
from lib.core import save_result
from lib.utilities import is_dir, get_repo_path


def process_arguments():
    """
    Uses the argparse module to parse commandline arguments.

    Returns:
        Dictionary of parsed commandline arguments.
    """
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
        '-p',
        '--plugins',
        type=is_dir,
        default='attributes',
        dest='plugins_dir',
        help='Path to the folder containing your set of plugins'
    )
    parser.add_argument(
        '-d',
        '--repositories-dir',
        type=is_dir,
        dest='repositories_dir',
        help='Path to the collection of downloaded repositories.'
    )
    parser.add_argument(
        '-s',
        '--repositories-sample',
        type=argparse.FileType('r'),
        dest='repositories_sample',
        help='A file containing newline-separated GHTorrent project ids'
    )
    parser.add_argument(
        '-k',
        '--key-string',
        type=str,
        dest='key_string',
        default=None,
        required=False,
        help='String of attribute initials. Uppercase to persist data'
    )
    parser.add_argument(
        '-n',
        '--num-processes',
        type=int,
        dest='num_processes',
        default=1,
        required=False,
        help=(
            'Number of processes to spawn when processing repositories'
            ' from the samples file.'
        )
    )

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()


def digits_in(num): return len(str(num))


def main():
    """
    Main execution flow.
    """
    args = process_arguments()

    sample = [int(line) for line in args.repositories_sample]
    # Digits in the size of the sample
    digits = digits_in(len(sample))

    config = process_configuration(args.config_file)
    db_settings = config['options']['datasource']
    (threshold, attributes) = process_plugins(args.plugins_dir)

    # If a keystring exists, then this function will overwrite enabled/persist
    # states based on the keystring
    process_key_string(attributes, args.key_string)
    attributes_copy = copy.deepcopy(attributes)

    (reporting, persist_attrs) = get_persist_attrs(attributes)
    report = []

    connection = establish_database_connection(db_settings)

    # Do before any multiprocessing
    load_attribute_plugins(args.plugins_dir, attributes)

    # Do before any multiprocessing
    global_init_attribute_plugins(attributes, connection, sample)

    # Generate a run_id with which processes are to save results
    cursor = connection.cursor()
    run_id = get_run_id(cursor)
    cursor.close()

    run_str = 'Beginning execution with id {0}'.format(run_id)
    print('{0}\n{1}\n{0}'.format('=' * len(run_str), run_str))

    connection.close()

    with multiprocessing.Pool(args.num_processes) as pool:
        report = pool.starmap(
            process,
            [(
                run_id,
                repo_id,
                get_repo_path(repo_id, args.repositories_dir),
                db_settings,
                attributes_copy,
                args.plugins_dir,
                persist_attrs,
                threshold
            ) for repo_id in sample]
        )

    if reporting:
        report_name = "report_" + str(int(time.time())) + ".json"
        with open(report_name, 'w') as report_file:
            json.dump(report, report_file)


def process(run_id, repo_id, repo_path, db_settings, attributes, plugins_dir,
            persist_attrs, threshold):
    repo_result = {"id": repo_id}

    try:
        connection = establish_database_connection(db_settings)

        load_attribute_plugins(plugins_dir, attributes)
        init_attribute_plugins(attributes, connection)

        score, results = process_repository(
            repo_id,
            repo_path,
            attributes,
            connection
        )

        # Generate a green checkmark or red x using terminal escapes
        if score > threshold:
            result_char = '\033[92m✓\033[0m'
        else:
            result_char = '\033[91m✘\033[0m'

        print('[{0:>10s}] {1}'.format(str(repo_id), result_char))

        for attr, result in results.items():
            if attr in persist_attrs:
                repo_result[attr] = result
    except:
        sys.stderr.write('Exception\n\n')
        sys.stderr.write('Project:\n')
        sys.stderr.write('  ID   {0}\n'.format(repo_id))
        sys.stderr.write('  Path {0}\n\n'.format(repo_path))
        extype, exvalue, extrace = sys.exc_info()
        traceback.print_exception(extype, exvalue, extrace)
    finally:
        cursor = connection.cursor()
        save_result(run_id, repo_id, repo_result, cursor)
        cursor.close()
        connection.close()

    return repo_result

if __name__ == '__main__':
    main()
