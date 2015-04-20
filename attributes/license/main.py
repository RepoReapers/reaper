import json
import urllib
import urllib.request


def run(project_id, repo_path, cursor, **options):
    query = 'SELECT url FROM projects WHERE id = ' + str(project_id)
    cursor.execute(query)
    record = cursor.fetchone()

    full_url = record[0].rstrip()
    request = urllib.request.Request(
        full_url,
        headers={
            'Accept': 'application/vnd.github.drax-preview+json'
        }
    )

    try:
        response = urllib.request.urlopen(request)

        raw_data = response.readall().decode('utf-8')
        json_data = json.loads(raw_data)

        if 'license' in json_data:
            result = 1
        else:
            result = 0
    except urllib.request.HTTPError as e:
        result = 0

    return result
