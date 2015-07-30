import sys

from attributes.unit_test.discoverer import get_test_discoverer


def run(project_id, repo_path, cursor, **options):
    query = 'SELECT language FROM projects WHERE id = %d' % project_id
    cursor.execute(query)

    record = cursor.fetchone()
    discoverer = get_test_discoverer(language=record[0])
    proportion = discoverer.discover(repo_path)

    threshold = options.get('threshold', 0)

    return (proportion is not None and proportion >= threshold), proportion

if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
