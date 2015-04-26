from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import distutils.spawn
import importlib
import json
import mysql.connector
import queue
import sched
import time
from utilities import url_to_json

scheduler = BackgroundScheduler()
scheduler.start()
available_tokens = queue.Queue()


def init(tokens):
    global available_tokens

    for token in tokens:
        available_tokens.put(token)


def get_token():
    while True:
        token = available_tokens.get(block=True)

        status = url_to_json(
            'https://api.github.com/rate_limit?access_token=%s' % token
        )

        if status['resources']['core']['remaining'] > 0:
            available_tokens.put_nowait(token)
            return token
        else:
            scheduler.add_job(
                available_tokens.put_nowait,
                'date',
                args=[token],
                run_date=datetime.datetime.fromtimestamp(
                    status['resources']['core']['reset']
                )
            )


def tokenize(url):
    if url.startswith('https://api.github.com'):
        token = get_token()
        return '{0}?access_token={1}'.format(url, token)
    else:
        raise ValueError('url must be for the GitHub API')


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
                **attribute['options']
            )

            cursor.close()

            score += binary_result * attribute['weight']
            results[attribute['name']] = raw_result

            if ('essential' in attribute and
                    attribute['essential'] and
                    not result):
                score = 0
                break

    return score, results


def load_attribute_plugins(attributes):
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
                    'attributes.{0}.main'.format(attribute['name'])
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
    try:
        config = json.load(config_file)
        if 'options' in config and 'attributes' in config:
            for attribute in config['attributes']:
                if 'dependencies' in attribute:
                    for dependency in attribute['dependencies']:
                        if distutils.spawn.find_executable(dependency) is None:
                            print('Missing dependency for attribute {0}: \
                                    {1}'.format(attribute['name'], dependency))
                            sys.exit(1)
                if 'name' not in attribute:
                    attribute['enabled'] = False
                if 'enabled' not in attribute:
                    attribute['enabled'] = False
                if 'weight' not in attribute:
                    attribute['weight'] = 5
                if 'options' not in attribute:
                    attribute['options'] = {}
            init(config['options']['githubTokens'])
            return config
        else:
            print('Configuration is missing required keys. See the sample \
                configuration provided with the repository contents.')
            sys.exit(2)
    except:
        print('Malformatted or missing configuration.')
        sys.exit(2)
