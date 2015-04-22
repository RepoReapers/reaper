from attributes.unit_test.discoverer import TestDiscoverer


class PhpTestDiscoverer(TestDiscoverer):
    def __init__(self):
        print('PHP Test Discoverer')

    def discover(self, path):
        pass
