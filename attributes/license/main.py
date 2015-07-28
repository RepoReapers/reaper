from lib import utilities

LICENSE_PATTERNS = [
    'http://unlicense.org/',                           # The Unlicense
    'http://mozilla.org/MPL',                          # Mozilla Public License
    'The MIT License (MIT)',                           # The MIT License
    'GNU LESSER GENERAL PUBLIC LICENSE',               # GNU LGPL
    (
        'THE SOFTWARE IS PROVIDED \"AS IS\" AND THE '
        'AUTHOR DISCLAIMS ALL WARRANTIES'
    ),                                                 # ISC
    'GNU GENERAL PUBLIC LICENSE',                      # GNU GPL
    'Eclipse Public License',                          # Eclipse Public License
    (
        'THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT '
        'HOLDERS AND CONTRIBUTORS \"AS IS\"'
    ),                                                 # BSD 3- and 2-clause
    'Artistic License',                                # Artistic License
    'http://www.apache.org/licenses',                  # Apache License
    'GNU AFFERO GENERAL PUBLIC LICENSE',               # GNU AGPL
]


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

    if not result:
        for pattern in LICENSE_PATTERNS:
            if utilities.search(pattern, repo_path, ignorecase=True):
                result = True
                break

    return result, int(result)

if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
else:
    from lib.core import Tokenizer
    from lib.utilities import url_to_json
