import utilities
from attributes.unit_test.discoverer import TestDiscoverer

LANGUAGE = 'Javascript'


class JavaScriptTestDiscoverer(TestDiscoverer):
    def __init__(self):
        self.frameworks = [
            self.__mocha__
        ]

    def discover(self, path):
        pass
