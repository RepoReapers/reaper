import sys

from attributes.unit_test.discoverer import get_test_discoverer


def run(project_id, repo_path, cursor, **options):
    query = 'SELECT language FROM projects WHERE id = %d' % project_id
    cursor.execute(query)

    record = cursor.fetchone()
    discoverer = get_test_discoverer(language=record[0])
    proportion = discoverer.discover(repo_path)

    cursor.close()

    threshold = 0
    if 'threshold' in options:
        threshold = options['threshold']
    proportion = discoverer.discover(repo_path)

    return (proportion != -1 and proportion >= threshold, proportion)

if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
