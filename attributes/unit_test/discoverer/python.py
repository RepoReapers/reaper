from attributes.unit_test.discoverer import TestDiscoverer


class PythonTestDiscoverer(TestDiscoverer):
    def __init__(self):
        self.language = 'Python'
        self.languages = ['Python']
        self.extensions = ['*.py']
        self.frameworks = [
            self.__django_test__,
            self.__nose__,
            self.__unittest__,
        ]

    def __django_test__(self, path, sloc):
        pattern = '((from|import)(\s)(django\.test))'
        return self.measure(path, sloc, pattern)

    def __nose__(self, path, sloc):
        pattern = '((from|import)(\s)(nose))'
        return self.measure(path, sloc, pattern)

    def __unittest__(self, path, sloc):
        pattern = '((from|import)(\s)(unittest))'
        return self.measure(path, sloc, pattern)
