import sys

from core import Tokenizer
from utilities import url_to_json


def run(project_id, repo_path, cursor, **options):
    t_sub = options.get('sub')
    t_star = options.get('star')
    t_forks = options.get('forks')

    cursor.execute('''
        SELECT
            url
        FROM
            projects
        WHERE
            id = {0}
        '''.format(project_id))

    record = cursor.fetchone()

    tokenizer = Tokenizer()
    full_url = tokenizer.tokenize(record[0].rstrip())
    json_response = url_to_json(full_url)

    subscribers_count = json_response.get('subscribers_count', 0)
    stargazers_count = json_response.get('stargazers_count', 0)
    forks = json_response.get('forks', 0)

    result = False
    if (
            (subscribers_count >= t_sub and stargazers_count >= t_star) or
            (stargazers_count >= t_star and forks >= t_forks) or
            (subscribers_count >= t_sub and forks >= t_forks)
       ):
        result = True

    return (
        result,
        {
            'sub': subscribers_count,
            'star': stargazers_count,
            'forks': forks
        }
    )


if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
