from lib import utilities
from attributes.unit_test.discoverer import TestDiscoverer

LANGUAGE = 'Ruby'


class RubyTestDiscoverer(TestDiscoverer):
    def __init__(self):
        self.frameworks = [
            self.__minitest__,
            self.__rspec__,
            self.__ruby_unit_testing__,
        ]

    def __minitest__(self, path):
        proportion = None

        files = utilities.search(
            '(MiniTest::Unit::TestCase|Minitest::Test)',
            path, whole=True, include=['*.rb']
        )

        if files:
            # SLOC of source code
            sloc_code = utilities.get_loc(path)

            # SLOC of test code
            sloc_test = utilities.get_loc(path, files=files)

            if LANGUAGE in sloc_code and LANGUAGE in sloc_test:
                proportion = (
                    sloc_test[LANGUAGE]['sloc'] /
                    sloc_code[LANGUAGE]['sloc']
                )

        return proportion

    def __rspec__(self, path):
        proportion = None

        files = utilities.search(
            '(describe)(.*)(do)',
            path, include=['*.rb']
        )

        if files:
            # SLOC of source code
            sloc_code = utilities.get_loc(path)

            # SLOC of test code
            sloc_test = utilities.get_loc(path, files=files)

            if LANGUAGE in sloc_code and LANGUAGE in sloc_test:
                proportion = (
                    sloc_test[LANGUAGE]['sloc'] /
                    sloc_code[LANGUAGE]['sloc']
                )

        return proportion

    def __ruby_unit_testing__(self, path):
        proportion = None

        files = utilities.search(
            'Test::Unit::TestCase',
            path, whole=True, include=['*.rb']
        )

        if files:
            # SLOC of source code
            sloc_code = utilities.get_loc(path)

            # SLOC of test code
            sloc_test = utilities.get_loc(path, files=files)

            if LANGUAGE in sloc_code and LANGUAGE in sloc_test:
                proportion = (
                    sloc_test[LANGUAGE]['sloc'] /
                    sloc_code[LANGUAGE]['sloc']
                )

        return proportion
