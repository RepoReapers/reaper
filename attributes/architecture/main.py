from pygments import lexers, token, util
import networkx
import os
import subprocess

supported_languages = []


def init(cursor):
    global supported_languages

    ctags_process = subprocess.Popen(
        ['ctags', '--list-languages'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    lines, _ = [x.decode('utf-8') for x in ctags_process.communicate()]
    for line in lines.split('\n'):
        supported_languages.append(line.lower())


def run(project_id, repo_path, cursor, **options):
    language_sizes = get_loc(repo_path)
    size = sum([value['sloc'] for value in language_sizes.values()])

    # Immediately fail the attribute if `minimumSize` is not met.
    if size < options.get('minimumSize', 1000):
        return False, 0

    cursor.execute('''
        SELECT
            language
        FROM
            projects
        WHERE
            id = {0}
        '''.format(project_id))

    record = cursor.fetchone()
    language = record[0]

    language = language.lower() if language else language

    # Edge case if the repository language is not supported by us.
    if language not in supported_languages:
        return False, 0

    ctags_process = subprocess.Popen(
        ['ctags', '-Rx', "--languages={0}".format(language), repo_path],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # TODO: Handle errors emitted by `ctags`.
    lines, _ = [
        x.decode(errors='replace') for x in ctags_process.communicate()
    ]

    file_names = set()
    for line in lines.split('\n'):
        fields = line.split()
        for field in fields:
            if os.path.isfile(field):
                file_names.add(field)

    graph = networkx.Graph()
    lexer = lexers.get_lexer_by_name(language)
    build_graph(file_names, graph, lexer)

    result = get_connectedness(graph)
    return result > options.get('connectedness', 0.75), result


def build_graph(file_names, graph, lexer):
    """
    for each file in the set of files
        create a node and add it to the graph
        open the file
        read the contents into memory
        get a list of tokens from the lexer
        for each token in the resulting tokens
            check if the token is defining a symbol
            if true, add the symbol to the file node

    for each file in the set of files
        open the file
        read the contents into memory
        get a list of token from the lexer
        for each token in the resulting tokens
            check if the token is using a symbol
            if true:
                search the graph for the node that has the symbol definition
                create a relationship from the current file to the node with
                the symbol definition
    """
    for file_name in file_names:
        node = Node(file_name)
        graph.add_node(node)
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                contents = file.read()

            tokens = lexer.get_tokens(contents)
            for item in tokens:
                token_type = item[0]
                if token_type in [token.Name.Function, token.Name.Class]:
                    node.add_symbol(item[1], token_type)
            if 'DEBUG' in os.environ:
                print(node)
        except FileNotFoundError as e:
            continue
        except UnicodeDecodeError:
            continue

    for origin_node in graph.nodes():
        try:
            with open(origin_node.path, 'r', encoding='utf-8') as file:
                contents = file.read()

            tokens = lexer.get_tokens(contents)
            for item in tokens:
                name = item[1]
                token_type = item[0]
                if token_type not in [token.Name.Function, token.Name.Class]:
                    for node in graph.nodes_iter():
                        if origin_node is not node and node.has_symbol(name):
                            graph.add_edge(origin_node, node)
        except FileNotFoundError as e:
            print("Not found: " + origin_node.path)
        except UnicodeDecodeError:
            continue


def get_connectedness(graph):
    node_degrees = graph.degree()
    zero_degrees = len(
        [degree for key, degree in node_degrees.items() if degree is 0]
    )

    if len(node_degrees) > 0:
        return 1 - (zero_degrees / len(node_degrees))
    else:
        return 0


class Node():
    def __init__(self, path):
        self.path = path
        self.symbols = set()

    def add_symbol(self, symbol, symbol_type=token.Generic):
        self.symbols.add((symbol_type, symbol))

    def has_symbol(self, item):
        for symbol in self.symbols:
            if item == symbol[1]:
                return True
        return False

    def __hash__(self):
        return hash(self.path)

    def __eq__(self, other):
        return self.path == other.path

    def __str__(self):
        result = '\r'
        for symbol in self.symbols:
            symbol_str = '{0}: {1}\n'.format(symbol[0], symbol[1])
            result += symbol_str

        return "{0}\n{1}\n{2}".format(
            self.path,
            '=' * len(self.path),
            result
        )

if __name__ == '__main__':
    import importlib
    import json
    import mysql.connector
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from lib.utilities import get_loc

    os.environ['DEBUG'] = '1'

    with open('../../config.json', 'r') as file:
        config = json.load(file)

    mysql_config = config['options']['datasource']

    connection = mysql.connector.connect(**mysql_config)
    connection.connect()

    cursor = connection.cursor()
    init(None)
    result = run(sys.argv[1], sys.argv[2], cursor, threshold=0.75)
    cursor.close()

    connection.close()

    print(result)
else:
    from lib.utilities import get_loc
