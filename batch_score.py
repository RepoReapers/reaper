#!/usr/bin/env python3

import argparse
from core import load_attribute_plugins
from core import init_attribute_plugins
from core import establish_database_connection
from core import process_configuration
from core import process_key_string
from core import process_repository
from core import get_persist_attrs
import json
import time
import os
import sys
from utilities import is_dir


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

    if len(sys.argv) < 1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()


def main():
    """
    Main execution flow.
    """
    args = process_arguments()

    sample = [int(line) for line in args.repositories_sample]
    digits = len(str(len(sample)))  # digits in the size of the sample

    config = process_configuration(args.config_file)
    # If a keystring exists, then this function will overwrite enabled/persist
    # states based on the keystring
    process_key_string(config['attributes'], args.key_string)

    persist_attrs = get_persist_attrs(config['attributes'])
    reporting = (len(persist_attrs) > 0)
    report = []

    connection = establish_database_connection(config['options']['datasource'])

    attributes = config['attributes']
    load_attribute_plugins(attributes)
    init_attribute_plugins(attributes, connection)

    left = len(sample)
    for repo_id in sample:
        # Repository path is the subdir within the id folder whose name is
        # NOT metadata.json. That is, the path we're interested in is the
        # downloaded git source. If no such path exists, the repository path
        # is simply the path to the id folder.
        base_path = args.repositories_dir + str(repo_id) + "/"
        repo_path = base_path  # Default to this if we can't find the git repo
        for entry in os.listdir(base_path):
            if(entry != 'metadata.json'):
                repo_path += entry
                break

        score, results = process_repository(
            repo_id,
            repo_path,
            attributes,
            connection
        )

        if reporting:
            report_entry = {"id": repo_id}
            for attr, result in results.items():
                if attr in persist_attrs:
                    report_entry[attr] = float(result)
            report.append(report_entry)

        # Generate a green checkmark or red x using terminal escapes
        if score > config['options']['threshold']:
            result_char = '\033[92m✓\033[0m'
        else:
            result_char = '\033[91m✘\033[0m'

        # When we print the next status line, we will have finished one repo
        left -= 1

        # Number of repos left to process out of the total number
        cur = ('{:0>' + str(digits) + 'd}').format(left)
        tot = str(len(sample))
        sid = '{: >11d}'.format(repo_id)

        print('remaining [{cur} / {tot}] ght_id [{sid}] {res}'.format(
            cur=cur, tot=tot, sid=sid, res=result_char))

    if reporting:
        report_name = "report_" + str(int(time.time())) + ".json"
        with open(report_name, 'w') as report_file:
            json.dump(report, report_file)

if __name__ == '__main__':
    main()
