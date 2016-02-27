import sys

from lib import utilities


def run(project_id, repo_path, cursor, **options):
    threshold = options.get('threshold', 0)

    cursor.execute('SELECT url FROM projects WHERE id = {}'.format(project_id))
    record = cursor.fetchone()

    full_url = utilities.TOKENIZER.tokenize(record[0].rstrip())
    json_response = utilities.url_to_json(full_url)
    rresult = (
        json_response['stargazers_count']
        if 'stargazers_count' in json_response
        else None
    )
    bresult = True if rresult is not None and rresult >= threshold else False

    return bresult, rresult

if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
