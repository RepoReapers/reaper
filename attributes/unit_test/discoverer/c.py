from attributes.unit_test.discoverer import TestDiscoverer


class CTestDiscoverer(TestDiscoverer):
    def __init__(self):
        self.language = 'C'
        self.languages = ['C', 'C/C++ Header']
        self.extensions = ['*.c', '*.h']
        self.frameworks = [
            self.__assert__,
            self.__clar__,
            self.__glib__,
            self.__picotest__,
        ]

    def __assert__(self, path, sloc):
        pattern = '#include <assert.h>'
        return self.measure(path, sloc, pattern, whole=True)

    def __clar__(self, path, sloc):
        pattern = '#include "clar.h"'
        return self.measure(path, sloc, pattern, whole=True)

    def __glib__(self, path, sloc):
        pattern = '(g_assert*|g_test*|GTest*)'
        return self.measure(path, sloc, pattern, whole=True)

    def __picotest__(self, path, sloc):
        pattern = '#include "picotest.h"'
        return self.measure(path, sloc, pattern, whole=True)
