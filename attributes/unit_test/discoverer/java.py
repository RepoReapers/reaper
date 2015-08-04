from attributes.unit_test.discoverer import TestDiscoverer


class JavaTestDiscoverer(TestDiscoverer):
    def __init__(self):
        self.language = 'Java'
        self.languages = ['Java']
        self.extensions = ['*.java']
        self.frameworks = [
            self.__junit__,
            self.__testng__
        ]

    def __junit__(self, path, sloc):
        pattern = 'import (org.junit|junit.framework)'
        return self.measure(path, sloc, pattern)

    def __testng__(self, path, sloc):
        pattern = 'import org.testng'
        return self.measure(path, sloc, pattern)
