from attributes.unit_test.discoverer import TestDiscoverer


class SwiftTestDiscoverer(TestDiscoverer):
    def __init__(self):
        self.language = 'Swift'
        self.languages = ['Swift']
        self.extensions = ['*.swift']
        self.frameworks = [
            self.__xctest__
        ]

    def __xctest__(self, path, sloc):
        pattern = 'XCTest'
        return self.measure(path, sloc, pattern, whole=True)
