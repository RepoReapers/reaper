import sys

from dateutil import relativedelta


def run(project_id, repo_path, cursor, **options):
    avg_commits = 0

    cursor.execute(
        '''
            SELECT COUNT(c.id), MIN(c.created_at), MAX(c.created_at)
            FROM commits c
                JOIN project_commits pc ON pc.commit_id = c.id
            WHERE pc.project_id = {0} and c.created_at > 0
        '''.format(project_id)
    )

    result = cursor.fetchone()
    num_commits = result[0]
    first_commit_date = result[1]
    last_commit_date = result[2]

    if first_commit_date is None or last_commit_date is None:
        return False, avg_commits

    # Compute the number of months between the first and last commit
    delta = relativedelta.relativedelta(last_commit_date, first_commit_date)
    num_months = delta.years * 12 + delta.months

    if num_months >= options.get('minimumDurationInMonths', 0):
        avg_commits = num_commits / num_months
    else:
        return False, avg_commits

    threshold = options['threshold']
    return avg_commits >= threshold, avg_commits

if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
