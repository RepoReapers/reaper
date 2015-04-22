from attributes.unit_test.discoverer import TestDiscoverer


class RubyTestDiscoverer(TestDiscoverer):
    def __init__(self):
        print('Ruby Test Discoverer')

    def discover(self, path):
        pass
