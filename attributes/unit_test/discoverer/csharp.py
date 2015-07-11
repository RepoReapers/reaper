from lib import utilities
from attributes.unit_test.discoverer import TestDiscoverer

LANGUAGE = 'C#'


class CSharpTestDiscoverer(TestDiscoverer):
    def __init__(self):
        self.frameworks = [
            self.__nunit__
        ]

    def __nunit__(self, path):
        proportion = -1

        files = utilities.search(
            'using NUnit.Framework;',
            path, include=['*.cs']
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
