from attributes.unit_test.discoverer import TestDiscoverer


class ObjectiveCTestDiscoverer(TestDiscoverer):
    def __init__(self):
        self.language = 'Objective C'
        self.languages = ['Objective C', 'C/C++ Header']
        self.extensions = ['*.m', '*.h']
        self.frameworks = [
            self.__xctest__
        ]

    def __xctest__(self, path, sloc):
        pattern = 'XCTest.h'
        return self.measure(path, sloc, pattern, whole=True)
