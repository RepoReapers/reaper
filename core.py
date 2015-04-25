import importlib
import json
import mysql.connector


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
