from attributes.unit_test.discoverer import TestDiscoverer


class CppTestDiscoverer(TestDiscoverer):
    def __init__(self):
        self.language = 'C++'
        self.languages = ['C++', 'C/C++ Header']
        self.extensions = ['*.c*', '*.h*']
        self.frameworks = [
            self.__assert__,
            self.__boost__,
            self.__catch__,
            self.__gtest__,
            self.__stout_gtest__
        ]

    def __assert__(self, path, sloc):
        pattern = '#include <assert.h>'
        return self.measure(path, sloc, pattern, whole=True)

    def __boost__(self, path, sloc):
        pattern = (
            '(BOOST_TEST_ALTERNATIVE_INIT_API|boost/test/unit_test.hpp|'
            'boost/test/included/unit_test.hpp|BOOST_TEST_DYN_LINK)'
        )
        return self.measure(path, sloc, pattern, whole=True)

    def __catch__(self, path, sloc):
        pattern = '#include "catch.hpp"'
        return self.measure(path, sloc, pattern, whole=True)

    def __gtest__(self, path, sloc):
        pattern = '#include (<|")(gtest/)?gtest.h(>|")'
        return self.measure(path, sloc, pattern, whole=True)

    def __stout_gtest__(self, path, sloc):
        pattern = '#include <stout/gtest.hpp>'
        return self.measure(path, sloc, pattern, whole=True)
