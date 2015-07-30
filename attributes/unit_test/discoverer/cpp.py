from lib import utilities
from attributes.unit_test.discoverer import TestDiscoverer

LANGUAGES = 'C++,C/C++ Header'


class CppTestDiscoverer(TestDiscoverer):
    def __init__(self):
        self.frameworks = [
            self.__assert__,
            self.__boost__,
            self.__catch__,
            self.__gtest__,
            self.__stout_gtest__
        ]

    def __assert__(self, path):
        proportion = None

        files = utilities.search(
            '#include <assert.h>',
            path, whole=True, include=['*.c*', '*.h*']
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

    def __boost__(self, path):
        proportion = None

        files = utilities.search(
            '(BOOST_TEST_ALTERNATIVE_INIT_API|boost/test/unit_test.hpp|'
            'boost/test/included/unit_test.hpp|BOOST_TEST_DYN_LINK)',
            path, whole=True, include=['*.c*', '*.h*']
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

    def __catch__(self, path):
        proportion = None

        files = utilities.search(
            '#include "catch.hpp"',
            path, whole=True, include=['*.c*', '*.h*']
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

    def __gtest__(self, path):
        proportion = None

        files = utilities.search(
            '#include (<|")(gtest/)?gtest.h(>|")',
            path, whole=True, include=['*.c*', '*.h*']
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

    def __stout_gtest__(self, path):
        proportion = None

        files = utilities.search(
            '#include <stout/gtest.hpp>',
            path, whole=True, include=['*.c*', '*.h*']
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
