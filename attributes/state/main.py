import sys
from datetime import datetime
from time import strptime
from lib import utilities
import os
import os as inner_os
from lib import dateutil

def get_last_commit_date(repo_path):   
    os.chdir(repo_path)
    stream = inner_os.popen('git log --pretty=format:%cd').read().split("\n")
    dat = stream[0].split(" ")
    page = dat[4] + "-" + str(strptime(dat[1],'%b').tm_mon) + "-" + dat[2]     
    return page

def run(project_id, repo_path, cursor, **options):
    print("----- METRIC: STATE -----")
    bresult = False
    rresult = 'dormant'
    # Obtaining last commit date 
    last_commit_date = get_last_commit_date(repo_path)
    if last_commit_date is not None:
        today = options.get('today', datetime.today().date())
        if isinstance(today, str):
            today = datetime.strptime(today, '%Y-%m-%d')
        last_commit_date_formatted = tuple(map(int,last_commit_date.split("-")))
        delta = dateutil.relativedelta(today, datetime(*last_commit_date_formatted))
        threshold = utilities.parse_datetime_delta(options['threshold'])
        bresult = delta <= threshold
        if bresult:
            rresult = 'active'
    print('State: ',rresult)
    return bresult, rresult

if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
