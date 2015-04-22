from attributes.unit_test.discoverer import TestDiscoverer


class ObjectiveCTestDiscoverer(TestDiscoverer):
    def __init__(self):
        print('Objective-C Test Discoverer')

    def discover(self, path):
        pass
