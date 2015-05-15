def run(project_id, repo_path, cursor, **options):
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
    json_response = url_to_json(full_url, headers={
            'Accept': 'application/vnd.github.drax-preview+json'
        }
    )

    result = True if 'license' in json_response \
                     and json_response['license'] else False

    return result, int(result)

if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
else:
    from lib.core import Tokenizer
    from lib.utilities import url_to_json
