import collections
import sys

from lib.core import Tokenizer
from lib.utilities import url_to_json


# Query counts the number of distinct authors contributing to a project.
QUERY = '''
    SELECT c.author_id, COUNT(*)
    FROM commits c JOIN project_commits pc
      ON pc.commit_id = c.id
    WHERE pc.project_id = {0}
    GROUP BY c.author_id
    ORDER BY COUNT(*) DESC
'''


def run(project_id, repo_path, cursor, **options):
    num_core_contributors = None

    cursor.execute(QUERY.format(project_id))
    rows = cursor.fetchall()
    if cursor.rowcount == 0:    # Non-existent history
        return False, num_core_contributors

    commits = collections.OrderedDict()
    for row in rows:
        commits[row[0]] = row[1]
    num_commits = sum(commits.values())

    cutoff = options.get('cutoff', 1.0)
    aggregate = 0
    num_core_contributors = 0
    for (_, v) in commits.items():
        num_core_contributors += 1
        aggregate += v
        if (aggregate / num_commits) >= cutoff:
            break

    threshold = options.get('threshold', 1)
    return (num_core_contributors >= threshold, num_core_contributors)


if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
