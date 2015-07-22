import sys

from lib.core import Tokenizer
from lib.utilities import url_to_json


# Query counts the number of distinct authors contributing to a project.
QUERY = '''
    SELECT COUNT(DISTINCT(c.author_id))
    FROM commits c JOIN project_commits pc
      ON pc.commit_id = c.id
    WHERE pc.project_id = {0}
'''


def run(project_id, repo_path, cursor, **options):
    cursor.execute(QUERY.format(project_id))
    record = cursor.fetchone()
    num_authors = record[0]
    threshold = options.get('threshold', 1)

    return (int(num_authors >= threshold), num_authors)


if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
