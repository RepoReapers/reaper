import sys
import os
from subprocess import Popen, PIPE

def run(project_id, repo_path, cursor, **options):
    print("----- METRIC: COMMUNITY -----")
    num_core_contributors = 0
    num_commits = 0
    commit_list = []

    # Collecting author email for every commit via git-shell command
    os.chdir(repo_path)
    with Popen(r'git log --pretty="%ae" | sort',shell=True,
            stdout=PIPE, stderr=PIPE) as p:
            output, errors = p.communicate()
    stream = output.decode('utf-8-sig',errors='ignore').splitlines()
    authors = set(stream)
    for names in authors:
        stream.count(names)
        commit_list.append(int(stream.count(names)))
        num_commits += int(stream.count(names))
    commit_list.sort(reverse=True) # commit_list contains the commits made by individual authors sorted in descending order
    
    cutoff = 0.8
    aggregate = 0
    for v in commit_list:
        num_core_contributors += 1
        aggregate += v
        if (aggregate / num_commits) >= cutoff:
            break
    print('# of Core Contributors: ',num_core_contributors)
    threshold = options['threshold']
    num_core_contributors >= threshold, num_core_contributors
    return (num_core_contributors >= threshold, num_core_contributors)


if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
