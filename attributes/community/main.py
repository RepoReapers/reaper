import sys
import json
import mysql.connector
import os
import urllib


def run(project_id, repo_path, cursor, **options):
	id = project_id
    cursor1 = connection.cursor(buffered = True)
    cursor2 = connection.cursor(buffered = True)    
    #Query 1
	query1 = "select count(f.follower_id) from followers f join project_members p on f.user_id = p.user_id and p.repo_id={0} group by p.repo_id;".format(id)
    cursor.execute(query1)
    result1 = cursor.fetchone()
    #Query 2
    query2 = "select count(user_id) from watchers where repo_id={0} group by repo_id;".format(id)
    cur2.execute(query2)
    result2 = cur2.fetchone()

    if result1 is None or result2 is None:
        return False
    elif int(result1[0]) > 5 and int(result2[0]) > 1:
        return True
    else:
        return False










if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    
