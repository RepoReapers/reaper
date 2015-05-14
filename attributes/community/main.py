import sys
import json
import mysql.connector
import os
import urllib


def run(project_id, repo_path, cursor, **options):
    id = project_id
    cursor = connection.cursor()
    query = "select count(user_id) from watchers where repo_id={0} group by repo_id;".format(id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    elif int(result[0]) > 1:
        return True
    else:
        return False


if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    
