from lib import utilities
from attributes.unit_test.discoverer import TestDiscoverer

LANGUAGES = 'Objective C,Objective C++,C/C++ Header'


class ObjectiveCTestDiscoverer(TestDiscoverer):
    def __init__(self):
        self.frameworks = [
            self.__xctest__
        ]

    def __xctest__(self, path):
        proportion = 0

        files = utilities.search(
            'XCTest.h',
            path, whole=True, include=['*.m', '*.h']
        )

        if files:
            # SLOC of source code
            sloc_code = utilities.get_loc(path)

            # SLOC of test code
            sloc_test = utilities.get_loc(path, files=files)

            _sloc_code = 0
            _sloc_test = 0

            for language in LANGUAGES.split(','):
                if language in sloc_code:
                    _sloc_code += sloc_code[language]['sloc']
                if language in sloc_test:
                    _sloc_test += sloc_test[language]['sloc']

            if _sloc_code != 0:
                proportion = _sloc_test / _sloc_code

        return proportion
