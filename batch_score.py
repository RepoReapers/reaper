#!/usr/bin/env python3

import argparse
import sys
import traceback

from lib import core, utilities, run
from lib.attributes import Attributes
from lib.database import Database


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
        '--cleanup',
        action='store_true',
        dest='cleanup',
        help='Delete cloned repositories from the disk when done.'
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
        '-m',
        '--manifest',
        type=argparse.FileType('r'),
        default='manifest.json',
        dest='manifest_file',
        help='Path to the manifest file.'
    )
    parser.add_argument(
        '-r',
        '--repositories-root',
        type=utilities.is_dir,
        dest='repositories_root',
        help='Path to the root of downloaded repositories.'
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


def main():
    """
    Main execution flow.
    """
    try:
        args = process_arguments()

        config = utilities.read(args.config_file)
        manifest = utilities.read(args.manifest_file)

        # TODO: Refactor
        core.config = config

        database = Database(config['options']['datasource'])
        globaloptions = {
            'today': config['options']['today'],
            'timeout': config['options']['timeout']
        }
        attributes = Attributes(
            manifest['attributes'], database, args.cleanup, args.key_string,
            **globaloptions
        )

        _run = run.Run(
            args.repositories_root, attributes, database,
            config['options']['threshold'], args.num_processes
        )
        _run.run([int(line) for line in args.repositories_sample])
    except Exception as e:
        extype, exvalue, extrace = sys.exc_info()
        traceback.print_exception(extype, exvalue, extrace)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\rCaught interrupt, killing all children...')
