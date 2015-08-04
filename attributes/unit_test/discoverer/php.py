from attributes.unit_test.discoverer import TestDiscoverer


class PhpTestDiscoverer(TestDiscoverer):
    def __init__(self):
        self.language = 'PHP'
        self.languages = ['PHP']
        self.extensions = ['*.php']
        self.frameworks = [
            self.__phpunit__
        ]

    def __phpunit__(self, path, sloc):
        pattern = 'PHPUnit_(Framework|Extensions_Database)_TestCase'
        return self.measure(path, sloc, pattern)
