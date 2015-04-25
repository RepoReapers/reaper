from utilities import url_to_json


def run(project_id, repo_path, cursor, **options):
    query = 'SELECT url FROM projects WHERE id = ' + str(project_id)
    cursor.execute(query)
    record = cursor.fetchone()

    full_url = record[0].rstrip()
    json_response = url_to_json(full_url)

    if 'license' in json_response:
        result = 1
    else:
        result = 0

    return result

if __name__ == '__main__':
    print("Attribute plugins are not meant to be executed directly.")
