import sys
import json
import mysql.connector
import os
import urllib


def run(project_id, repo_path, cursor, **options):
    id=project_id 
    query = "SELECT count(id) as total, DATEDIFF(max(created_at), min(created_at)) as Days from commits where project_id={0} and created_at>0;".format(id)
    cursor.execute(query)
    result = cursor.fetchone()
	d1=float(result[0]) #total number of commits
	d2=float(result[1]) #total number of days	
    week=d2/7           #calculate total number of weeks
	if week < 1:
        return 0
	else:
	    ans = round(d1/week)
        if ans < 2:
        	return 0
        else: 
        	return 1
	    
    


if __name__ == '__main__':
    print("Attribute plugins are not meant to be executed directly.") 
