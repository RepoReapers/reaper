import sys

from dateutil import relativedelta


def run(project_id, repo_path, cursor, **options):
    avg_issues = 0

    cursor.execute(
        '''
            SELECT MIN(c.created_at), MAX(c.created_at)
            FROM commits c
                JOIN project_commits pc ON pc.commit_id = c.id
            WHERE pc.project_id = {0} and c.created_at > 0
        '''.format(project_id)
    )

    result = cursor.fetchone()
    first_commit_date = result[0]
    last_commit_date = result[1]

    if first_commit_date is None or last_commit_date is None:
        return False, avg_issues

    cursor.execute(
        '''
            SELECT COUNT(*)
            FROM issues i
            WHERE i.repo_id = {0}
        '''.format(project_id)
    )

    result = cursor.fetchone()
    num_issues = result[0]

    # Compute the number of months between the first and last commit
    delta = relativedelta.relativedelta(last_commit_date, first_commit_date)
    num_months = delta.years * 12 + delta.months

    if num_months >= options.get('minimumDurationInMonths', 0):
        avg_issues = num_issues / num_months
    else:
        return False, avg_issues

    threshold = options['threshold']
    return avg_issues >= threshold, avg_issues

if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
