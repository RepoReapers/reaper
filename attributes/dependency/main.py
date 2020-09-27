import sys
import os
import os as inner_os
import arrow
from time import strptime
from datetime import datetime
import platform

def run(project_id, repo_path, cursor, **options):
    print("----- METRIC: DEPENDENCY -----")
    num_core_commits = 0
    dependency_ratio_total = 0
    total_lines = 0
    os.chdir(repo_path)
    abs_files = []
    Files = []
    # Finding all the library dependency files
    for (root,dirs,files) in inner_os.walk(os.getcwd(),topdown=True):
        for fi in files:
            if fi.endswith(".yml"):
                Files.append(files)
                abs_files.append(os.path.join(root,fi))
            elif fi.endswith(".json"):
                Files.append(files)
                abs_files.append(os.path.join(root,fi))    
            elif fi.endswith(".gradle"):
                Files.append(files)
                abs_files.append(os.path.join(root,fi))
    # Getting the commit ids and commit dates for each library dependency file
    for filename in abs_files:
        if(platform.system() == 'Windows'):
            filename = filename.replace(os.getcwd()+'\\','')
        else:
            filename = filename.replace(os.getcwd()+'/','')
        stream = inner_os.popen('git log '+ filename +'').read().split("\n")
        commit_id = []
        year = []
        month = []
        day = []
        length = 0
        version_dependencies = []
        changes = 0
        for lines in stream:
            if("commit" in lines):
                if(lines.index("commit") == 0):
                    commit_id.append(lines.split(" ")[1])
                    length += 1
            elif("Date:" in lines):
                date_id = lines.split("Date:")[1].split(" ")
                month.append(int(strptime(date_id[4],'%b').tm_mon))
                day.append(int(date_id[5]))
                year.append(int(date_id[7]))
        end = datetime(year[0],month[0],day[0])
        for a in range(1,length-1):
            n_months = -1
            start = datetime(year[length-1-a],month[length-1-a],day[length-1-a])
            for d in arrow.Arrow.range('month',start,end):
                n_months += 1
            if(n_months <= 12):
                # Obtaining the code difference between the latest commit and last commit within the last one year 
                stream2 = inner_os.popen('git diff '+commit_id[length-1-a]+" " + commit_id[0] +" -- "+ filename +"").read().split("\n")
                if(len(stream2) > 0):
                    ind = 0
                    for z in stream2:
                        ind += 1
                        if("@@" in z):
                            break
                    for z in range(ind,len(stream2)):
                        if("+" in stream2[z]):
                            if(stream2[z].index("+") == 0):
                                if("0." in stream2[z] or "1." in stream2[z] or "2." in stream2[z] or "3." in stream2[z] or "4." in stream2[z] or "5." in stream2[z] or "6." in stream2[z] or "7." in stream2[z] or "8." in stream2[z] or "9." in stream2[z]):
                                    changes += 1
                break
        total_number_of_dependency_lines = 0
        fp = open(filename,'r')
        for x in fp:
            if("0." in x or "1." in x or "2." in x or "3." in x or "4." in x or "5." in x or "6." in x or "7." in x or "8." in x or "9." in x):
                total_number_of_dependency_lines += 1
        dependency_ratio_total += changes
        total_lines += total_number_of_dependency_lines 
    threshold = options['threshold']
    if(total_lines > 1):
        dependency_ratio_total = float(dependency_ratio_total)/(total_lines*1.0)
    print('Dependency Score: ',dependency_ratio_total)  
    return (dependency_ratio_total >= threshold, dependency_ratio_total)
if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
