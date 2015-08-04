import sys
from datetime import datetime

from lib import dateutil
from lib import utilities


def run(project_id, repo_path, cursor, **options):
    cursor.execute(
        '''
            SELECT MAX(c.created_at)
            FROM commits c
                JOIN project_commits pc ON pc.commit_id = c.id
            WHERE pc.project_id = {0} and c.created_at > 0
        '''.format(project_id)
    )

    result = cursor.fetchone()
    last_commit_date = result[0]

    # Compute the delta between the last commit in the database and today.
    # Note: today may be the date the GHTorrent dump was published by
    #       ghtorrent.org
    today = options.get('today', datetime.today().date())
    if isinstance(today, str):
        today = datetime.strptime(today, '%Y-%m-%d')
    delta = dateutil.relativedelta(today, last_commit_date)

    threshold = utilities.parse_datetime_delta(options['threshold'])
    return delta <= threshold, 'active' if delta <= threshold else 'dormant'

if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
