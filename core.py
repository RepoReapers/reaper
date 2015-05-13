import apscheduler.schedulers.background
import datetime
import distutils.spawn
import importlib
import json
import mysql.connector
import queue
import time
import sys
import pprint
from utilities import url_to_json

tokens = []


class Tokenizer():
    def __init__(self):
        self.have_tokens = bool(tokens)
        self.available_tokens = queue.Queue()
        self.scheduler = apscheduler.schedulers.background.BackgroundScheduler(
            )
        self.scheduler.start()

        if not self.have_tokens:
            self.print_warning(
                'No GitHub OAuth tokens provided. Proceeding without '
                'authentication.'
            )

        for token in tokens:
            self.available_tokens.put(token)

    def tokenize(self, url):
        if url.startswith('https://api.github.com'):
            if self.have_tokens:
                token = self.get_token()
                if token is not None:
                    return '{0}?access_token={1}'.format(url, token)
                else:
                    return url
            else:
                return url
        else:
            raise ValueError('url must be for the GitHub API')

    def get_token(self):
        while True:
            if not self.scheduler.get_jobs() and self.available_tokens.empty():
                self.print_warning('No more valid OAuth tokens available.')
                return None

            token = self.available_tokens.get(block=True)

            rate_limit_url = (
                'https://api.github.com/rate_limit?access_token={0}'
            ).format(token)
            status = url_to_json(rate_limit_url)

            # Throw away bad OAuth keys.
            if 'resources' not in status:
                self.print_warning(
                    'Invalid OAuth token supplied. Trying again...'
                )
                continue

            if status['resources']['core']['remaining'] > 0:
                self.available_tokens.put_nowait(token)
                return token
            else:
                self.scheduler.add_job(
                    self.available_tokens.put_nowait,
                    'date',
                    args=[token],
                    run_date=datetime.datetime.fromtimestamp(
                        status['resources']['core']['reset']
                    )
                )

    def print_warning(self, message):
        formatted_message = '\033[91mWARNING\033[0m: {0}'.format(message)
        print(formatted_message)


def save_result(repo_id, results, cursor):
    """
    Save the results to the specified data source, creating the results table
    as necessary.

    Args:
        repo_id: int
            Identifier of the repository to save.
        results: dict
            Key value pair of results to be saved.
        cursor: mysql.cursor.MySQLCursor
            Cursor object used to insert data.

    Return:
        True if successful, False otherwise.
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


def init_attribute_plugins(attributes, connection):
    for attribute in attributes:
        if 'implementation' in attribute:
            try:
                cursor = connection.cursor()
                attribute['implementation'].init(cursor)
            except:
                pass
            finally:
                cursor.close()


def global_init_attribute_plugins(attributes, connection, sample):
    for attribute in attributes:
        if 'implementation' in attribute:
            try:
                cursor = connection.cursor()
                attribute['implementation'].global_init(cursor, sample)
            except:
                pass
            finally:
                cursor.close()


def process_repository(project_id, repo_path, attributes, connection):
    """
    Calculate a score for the given repository.

    Args:
        project_id: int
            GHTorrent dataset identifier for the repository.
        repo_path: string
            Path to the repository contents.
        attributes: list
            List of attributes to be executed against the repository.
        connection: mysql.connector.MySQLConnection
            Database connection used for querying the GHTorrent dataset.
    """
    score = 0
    results = {}
    for attribute in attributes:
        if 'implementation' in attribute:
            cursor = connection.cursor()

            binary_result, raw_result = attribute['implementation'].run(
                project_id,
                repo_path,
                cursor,
                **attribute.get('options', {})
            )

            cursor.close()

            score += binary_result * attribute['weight']
            results[attribute['name']] = raw_result

            if ('essential' in attribute and
                    attribute['essential'] and
                    not binary_result):
                score = 0
                break

    return score, results


def load_attribute_plugins(plugins_dir, attributes):
    """
    Attempt to load each of the attributes as defined in the configuration
    file.

    Args:
        attributes: list
            List of attribute dictionaries with the specific configuration
            data.
    """
    for attribute in attributes:
        if attribute['enabled']:
            try:
                attribute['implementation'] = importlib.import_module(
                    '{0}.{1}.main'.format(plugins_dir, attribute['name'])
                )

            except ImportError:
                print('Failed to load the {0} attribute.'.format(
                        attribute['name']
                    )
                )


def establish_database_connection(config):
    """
    Attempt to establish a connection to the specified database. Exit with an
    error message on failure.

    Args:
        config: dict
            Settings for the database connection.
    """
    try:
        connection = mysql.connector.connect(**config)
        connection.connect()
        return connection
    except mysql.connector.Error:
        print('\rUnable to establish connection to database.')
        sys.exit(1)


def process_configuration(config_file):
    """
    Load and validate the given configuration file.

    Args:
        config_file: File
            File object with the configuration contents.

    Returns:
        Validated dictionary with configuration parameters.
    """
    global tokens

    try:
        config = json.load(config_file)
    except:
        print('Your config file is malformed, or does not exist!')
        sys.exit(1)
    finally:
        tokens = config['options'].get('github_tokens', [])
        return config


def process_plugins(plugins_dir):
    manifest = plugins_dir + '/manifest.json'
    try:
        with open(manifest, 'r') as f:
            plugins = json.load(f)

            attributes = plugins['attributes']
            threshold = plugins['threshold']
 
            for attribute in attributes:
                exit_if_dep_missing(attribute)

            return (threshold, attributes)
          
    except:
        print('{} is malformed, or does not exist!'.format(manifest))
        sys.exit(1)


def exit_if_dep_missing(attribute):
    if not attribute['enabled'] or 'dependencies' not in attribute:
        dependencies = []
    else:
        dependencies = attribute['dependencies']

    for dependency in dependencies:
        if not distutils.spawn.find_executable(dependency):
            print('Missing dependency for attribute {}: {}'
                .format(attribute['name'], dependency)
            )
            sys.exit(1)


def process_key_string(attributes, key_string):
    """Reprocesses the attribute configuration based on a keystring

    The keystring is a single string interpreted as a list of individual
    initials. Each initial indicates a particular attribute, as defined in
    config.json.

    If no keystring is provided, the attribute configuration is left untouched.
    If a keystring is provided, then first, all attributes are disabled. Only
    those attribtues referred by their initials in the keystring are
    re-enabled. Further, if the attribute initial in the keystring is
    capitalized, then that attribute's data will be persisted.
    """
    if key_string is None:
        return

    initials = dict()  # Attribute initial => attribute dict
    for attribute in attributes:
        initial = attribute['initial'].lower()
        initials[initial] = attribute
        attribute['enabled'] = False  # Disable all attributes first
        attribute['persistResult'] = False

    if key_string == "help":
        for key_low, attribute in initials.items():
            print(key_low + " " + attribute['name'])
        sys.exit()

    for key_raw in key_string:
        key_low = key_raw.lower()
        attribute = initials[key_low]
        # Enable attribute since its initial is in the keystring
        attribute['enabled'] = True
        # Persist results if the raw key is capitalized
        attribute['persistResult'] = (not key_raw == key_low)


def get_persist_attrs(attributes):
    persist_attrs = []
    for attribute in attributes:
        if attribute['persistResult']:
            persist_attrs.append(attribute['name'])

    return (len(persist_attrs) > 0, persist_attrs)
