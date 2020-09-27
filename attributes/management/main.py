import sys
from time import strptime
from datetime import datetime
import arrow
import os
from lib.utilities import url_to_dom_value

QUERY = '''
SELECT url FROM projects WHERE id={0}
'''
def run(project_id, repo_path, cursor, **options):
    print("----- METRIC: ISSUES -----")
    cursor.execute(QUERY.format(project_id))
    url = cursor.fetchone()[0].replace("api.","").replace("repos/","")
    open_url = url + "/issues?q=is%3Aopen+is%3Aissue"
    closed_url = url + "/issues?q=is%3Aissue+is%3Aclosed"
    closed_issues = 0
    open_issues = 0
    git_tokens = options['tokens']
    token_avail = False
    # Making a request for open issues count with the tokens provided
    for token in git_tokens:
        if(token_avail == True):
            break 
        else: 
            try:
                open_issues = url_to_dom_value(open_url,[git_tokens[token],token],"Open")
                token_avail = True
                break
            except:
                continue
    # Making a request for open issues count without token, in the case all OAuth tokens got expired or incorrect tokens provided  
    if(token_avail == False):
        try:
            open_issues = url_to_dom_value(open_url,"Open")
            print('without token - open issues - fetch ok')
        except Exception as ex:
            print(ex)
            open_issues = 0
    token_avail = False
    # Making a request for closed issues count with the tokens provided
    for token in git_tokens:
        if(token_avail == True):
            break 
        else: 
            try:
                closed_issues = url_to_dom_value(closed_url,[git_tokens[token],token],"Closed")
                token_avail = True
                break
            except:
                continue
    # Making a request for closed issues count without token, in the case all OAuth tokens got expired or incorrect tokens provided  
    if(token_avail == False):
        try:
            closed_issues = url_to_dom_value(closed_url,"Closed")
            print('without token - closed issues - fetch ok')
        except Exception as ex:
            print(ex)
            closed_issues = 0
    total_issues = open_issues + closed_issues
    num_months = -1
    # Obtaining total number of commits with dates via git-shell command
    os.chdir(repo_path)
    stream = os.popen('git log --pretty=format:"%cd"').read().split("\n")
    num_commits = len(stream)
    if(num_commits > 1):
        prev = stream[num_commits-1].split(" ")
        Y1 = int(prev[4])
        M1 = int(strptime(prev[1],'%b').tm_mon)
        D1 = int(prev[2])
        start = datetime(Y1,M1,D1)
        prev = stream[0].split(" ")
        Y1 = int(prev[4])
        M1 = int(strptime(prev[1],'%b').tm_mon)
        D1 = int(prev[2])
        end = datetime(Y1,M1,D1)
        # Calculating number of months between first and latest commit
        for d in arrow.Arrow.range('month', start, end):
            num_months += 1
    issue_frequency = 0
    if num_months >= 1:
        avg_issues = total_issues / num_months*1.0
        print('Issue Frequency: ',avg_issues)
    if num_months >= options.get('minimumDurationInMonths', 1):
        avg_issues = total_issues / num_months 
    else:
        return False, avg_issues
    threshold = options['threshold']
    return avg_issues >= threshold, avg_issues
        
if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
