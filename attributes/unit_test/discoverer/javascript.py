import utilities
from attributes.unit_test.discoverer import TestDiscoverer

LANGUAGE = 'Javascript'


class JavaScriptTestDiscoverer(TestDiscoverer):
    def __init__(self):
        self.frameworks = [
            self.__mocha__
        ]

    def __mocha__(self, path):
        proportion = -1

        if utilities.search('mocha', path, include=['package.json']):
            files = utilities.search(
                '(describe\()(.*)(function)',
                path, whole=True, include=['*.js'], exclude=['mocha.js']
            )

            if files:
                # SLOC of source code
                sloc_code = utilities.get_loc(path)

                # SLOC of test code
                sloc_test = utilities.get_loc(path, files=files)

                if LANGUAGE in sloc_code and LANGUAGE in sloc_test:
                    proportion = (
                        sloc_test[LANGUAGE]['sloc'] /
                        sloc_code[LANGUAGE]['sloc']
                    )

        return proportion
