import sys
from datetime import datetime

from lib import dateutil
from lib import utilities

QUERY = '''
    SELECT MAX(c.created_at)
    FROM commits c
        JOIN project_commits pc ON pc.commit_id = c.id
    WHERE pc.project_id = {0} and c.created_at > 0
'''


def run(project_id, repo_path, cursor, **options):
    bresult = False
    rresult = 'dormant'

    cursor.execute(QUERY.format(project_id))
    result = cursor.fetchone()
    last_commit_date = result[0]

    if last_commit_date is not None:
        # Compute the delta between the last commit in the database and today.
        # Note: today may be the date the GHTorrent dump was published by
        #       ghtorrent.org
        today = options.get('today', datetime.today().date())
        if isinstance(today, str):
            today = datetime.strptime(today, '%Y-%m-%d')
        delta = dateutil.relativedelta(today, last_commit_date)
        threshold = utilities.parse_datetime_delta(options['threshold'])
        bresult = delta <= threshold
        if bresult:
            rresult = 'active'

    return bresult, rresult

if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
