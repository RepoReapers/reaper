import glob


def run(project_id, repo_path, cursor, **options):
    results = glob.glob(repo_path + "/{LICENSE,COPYING,COPYING.TXT}")

    print(results)
