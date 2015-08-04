from attributes.unit_test.discoverer import TestDiscoverer


class JavaScriptTestDiscoverer(TestDiscoverer):
    def __init__(self):
        self.language = 'Javascript'
        self.languages = ['Javascript']
        self.extensions = ['*.js']
        self.frameworks = [
            self.__mocha__
        ]

    def __mocha__(self, path, sloc):
        pattern = '(describe\()(.*)(function)'
        return self.measure(path, sloc, pattern)
