from lib import utilities
from attributes.unit_test.discoverer import TestDiscoverer

LANGUAGE = 'PHP'


class PhpTestDiscoverer(TestDiscoverer):
    def __init__(self):
        self.frameworks = [
            self.__phpunit__
        ]

    def __phpunit__(self, path):
        proportion = None

        files = utilities.search(
            'PHPUnit_(Framework|Extensions_Database)_TestCase',
            path, whole=True, include=['*.php']
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
