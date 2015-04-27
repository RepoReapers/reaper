from pygments import lexers, token, util
import networkx
import os
import subprocess


def run(project_id, repo_path, cursor, **options):
    query = 'SELECT * FROM projects WHERE id = ' + str(project_id)
    cursor.execute(query)

    record = cursor.fetchone()
    language = record[5]

    ctags_process = subprocess.Popen(
        ['ctags', '-Rx', "--languages={0}".format(language), repo_path],
        stdout=subprocess.PIPE
    )

    ctags_output = ctags_process.stdout.readlines()
    file_names = get_language_files(ctags_output)

    graph = networkx.Graph()
    lexer = lexers.get_lexer_by_name(language)
    build_graph(file_names, graph, lexer)

    result = networkx.is_connected(graph)
    return result, int(result)


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
    for each node in the graph
        check if there exists a relationship with any other node in the graph

    if there is a node without any relationships, fail the architecture test
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
                token_type = item[0]
                if token_type not in [token.Name.Function, token.Name.Class]:
                    for node in graph.nodes_iter():
                        if node.has_symbol(item[1]):
                            graph.add_edge(origin_node, node)
        except FileNotFoundError as e:
            print("Not found")
        except UnicodeDecodeError:
            continue


def find_node_by_name(graph, name):
    for node, data in graph.nodes_iter(data=True):
        if data['name'] is name:
            return node
    return None


def get_language_files(ctags_output):
    result = set()

    for line in ctags_output:
        fields = line.decode('utf-8').split()
        result.add(fields[3])

    return result


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
    print('Attribute plugins are not meant to be executed directly.')
