import utilities
from attributes.unit_test.discoverer import TestDiscoverer

LANGUAGE = 'Ruby'


class RubyTestDiscoverer(TestDiscoverer):
    def __init__(self):
        self.frameworks = [
            self.__rspec__
        ]

    def __rspec__(self, path):
        proportion = -1

        if utilities.search('rspec', path, whole=True):
            files = utilities.search(
                '(describe)(.*)(do)',
                path, include=['*.rb']
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
