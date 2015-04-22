from attributes.unit_test.discoverer import TestDiscoverer


class JavaTestDiscoverer(TestDiscoverer):
    def __init__(self):
        print('Java Test Discoverer')

    def discover(self, path):
        pass
