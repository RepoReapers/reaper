from attributes.unit_test.discoverer import TestDiscoverer


class CppTestDiscoverer(TestDiscoverer):
    def __init__(self):
        print('C++ Test Discoverer')

    def discover(self, path):
        pass
