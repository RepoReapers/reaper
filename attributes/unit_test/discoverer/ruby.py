from attributes.unit_test.discoverer import TestDiscoverer


class RubyTestDiscoverer(TestDiscoverer):
    def __init__(self):
        self.language = 'Ruby'
        self.languages = ['Ruby']
        self.extensions = ['*.rb']
        self.frameworks = [
            self.__minitest__,
            self.__rspec__,
            self.__ruby_unit_testing__,
        ]

    def __minitest__(self, path, sloc):
        pattern = '(MiniTest::Unit::TestCase|Minitest::Test)'
        return self.measure(path, sloc, pattern, whole=True)

    def __rspec__(self, path, sloc):
        pattern = '(describe)(.*)(do)'
        return self.measure(path, sloc, pattern)

    def __ruby_unit_testing__(self, path, sloc):
        pattern = 'Test::Unit::TestCase'
        return self.measure(path, sloc, pattern, whole=True)
