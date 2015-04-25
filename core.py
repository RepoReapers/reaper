import importlib
import json
import mysql.connector


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


def process_repository(project_id, repo_path, attributes, connection):
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
