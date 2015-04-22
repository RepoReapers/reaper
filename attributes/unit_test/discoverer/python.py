from attributes.unit_test.discoverer import TestDiscoverer


class PythonTestDiscoverer(TestDiscoverer):
    def __init__(self):
        print('Python Test Discoverer')
