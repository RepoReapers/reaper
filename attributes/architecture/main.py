from pygments import lexers, token
import networkx
import os


def run(project_id, repo_path, cursor, **options):
    query = 'SELECT * FROM projects WHERE id = ' + str(project_id)
    cursor.execute(query)

    record = cursor.fetchone()
    language = record[5]

    graph = networkx.DiGraph()

    for root, dirs, file_names in os.walk(repo_path):
        for file_name in file_names:
            with open(file, 'r') as file:
                content = file.read()
            lexer = lexers.guess_lexer(content)
            for token in lexer.get_tokens(content):
                if isinstance(token[0], token.Name.Function):
                    pass

    return 0

if __name__ == '__main__':
    print("Attribute plugins are not meant to be executed directly.")
