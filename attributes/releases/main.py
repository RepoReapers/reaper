import collections
import sys
import os
import arrow
from time import strptime
from datetime import datetime
import statistics

def time_gap(time2,time1):
    Y1 = int(time1[4])
    M1 = int(strptime(time1[1],'%b').tm_mon)
    D1 = int(time1[2])
    end = datetime(Y1,M1,D1)
    Y2 = int(time2[4])
    M2 = int(strptime(time2[1],'%b').tm_mon)
    D2 = int(time2[2])            
    start = datetime(Y2,M2,D2)
    num_days = -1
    for d in arrow.Arrow.range('day', start, end):
        num_days += 1
    return num_days                

def run(project_id, repo_path, cursor, **options):
    print("----- METRIC: RELEASES -----")
    # Obtaining release meta information via git-shell command
    os.chdir(repo_path)
    stream = os.popen('git for-each-ref --format="%(refname:short) | %(creatordate)" refs/tags/* --sort=creatordate').read().split("\n")
    total_releases = 0
    release_score = 0
    today = options.get('today', datetime.today().date())
    if isinstance(today, str):
        today = datetime.strptime(today, '%Y-%m-%d')
    release_gaps = []
    if(len(stream) > 3 ):
        if(len(stream)-2 > 0):
            for release in range(0,len(stream)-2):
                gap  = time_gap(stream[release].split("| ")[1].split(" "),stream[release+1].split("| ")[1].split(" "))
                release_gaps.append(gap)
            avg_release_time = statistics.mean(release_gaps) # In number of days
            standard_deviation = statistics.stdev(release_gaps)
            expected_release_gap = avg_release_time + standard_deviation # Expected Release gap is sum of average release gap and standard deviation
            time1 = stream[len(stream)-2].split("| ")[1].split(" ") # Latest release date
            Y1 = int(time1[4])
            M1 = int(strptime(time1[1],'%b').tm_mon)
            D1 = int(time1[2])
            end = datetime(Y1,M1,D1)
            time_now = str(today).split(" ")[0].split("-") # Time Now
            Y2 = int(time_now[0])
            M2 = int(time_now[1])
            D2 = int(time_now[2])
            now = datetime(Y2,M2,D2)
            days_passed = -1
            for d in arrow.Arrow.range('day',end,now):
                days_passed += 1
            if(days_passed <= expected_release_gap):
                release_score = 1
            print("Release Score: ",release_score)
    threshold = options['threshold']
    return (release_score >= threshold, release_score)


if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
