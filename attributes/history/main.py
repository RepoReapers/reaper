import sys
import os
from dateutil import relativedelta
from time import strptime
from datetime import datetime
import arrow

def run(project_id, repo_path, cursor, **options):
    print("----- METRIC: HISTORY -----")
    avg_commits = 0
    num_commits = 0
    # Obtaining total number of commits with dates via git-shell command
    os.chdir(repo_path)
    stream = os.popen('git log --pretty=format:"%cd"').read().split("\n")
    num_commits = len(stream)
    number_of_months = -1
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
            number_of_months += 1
        if(number_of_months != 0):
            avg_commits = float(num_commits)/(float(number_of_months)*1.0)
            print('Average Commits: ',avg_commits)
            threshold = options['threshold']
            return avg_commits >= threshold, avg_commits
        else:
            return False, avg_commits
    else:
        return False, avg_commits

if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
