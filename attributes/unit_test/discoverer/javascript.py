import utilities
from attributes.unit_test.discoverer import TestDiscoverer

LANGUAGE = 'Javascript'


class JavaScriptTestDiscoverer(TestDiscoverer):
    def __init__(self):
        print('JavaScript Test Discoverer')
