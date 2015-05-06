import sys
import json
import mysql.connector
import os
import urllib


def run(project_id, repo_path, cursor, **options):
    cursor.execute('''
        SELECT
            count(id),
            DATEDIFF(max(created_at), min(created_at))
        FROM
            commits
        WHERE
            project_id={0} and created_at > 0
        '''.format(project_id))

    result = cursor.fetchone()

    total_commits = int(result[0])
    total_days = int(result[1])
    total_weeks = total_days / 7

    min_weeks = options.get('minimumWeeks', 1)
    commits_per_week = total_commits / total_weeks if total_weeks > 0 else 0

    if total_weeks < min_weeks:
        return False, commits_per_week

    threshold = options.get('threshold', 2)

    return commits_per_week > threshold, commits_per_week

if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
