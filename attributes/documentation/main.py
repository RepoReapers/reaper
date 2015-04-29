import utilities

def run(project_id, repo_path, cursor, **options):
    util = utilities.get_loc(repo_path)
   
    sloc = 0
    cloc = 0
    for lang, metrics in util.items():
        sloc += metrics['sloc']
        cloc += metrics['cloc'] 

    ratio = cloc / sloc 

    attr_threshold = options['threshold']
    attr_pass = (ratio >= attr_threshold)

    return (attr_pass, ratio)

if __name__ == '__main__':
    print("Attribute plugins are not meant to be executed directly.")

    (attr_pass, ratio) = run(4324425, "/home/skroh/temp/fetched_repos/4324425",
None, threshold=2.0)

    print((attr_pass, ratio))
