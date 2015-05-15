import sys
import json
import mysql.connector
import os
import urllib


def run(project_id, repo_path, cursor, **options):
    id = project_id
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
    subscribers_count=json_response['subscribers_count']	
    stargazers_count=json_response['stargazers_count']
    forks=json_response['forks']
    sub = options.get('sub')
    star = options.get('star')
    forks = options.get('forks')			
    if (subscribers_count >= sub and stargazers_count >= star) or (stargazers_count >= star and forks >= forks) or (subscribers_count >= sub and forks >= forks):
        return (True,(subscribers_count,stargazers_count,forks))
    else: 					
        return (False,(subscribers_count,stargazers_count,forks))
    				
    	


if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
else:
    from core import Tokenizer
    from utilities import url_to_json    
