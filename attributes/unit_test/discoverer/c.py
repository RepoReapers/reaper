import utilities
from attributes.unit_test.discoverer import TestDiscoverer

# TODO: Include header files as well
LANGUAGE = 'C'


class CTestDiscoverer(TestDiscoverer):
    def __init__(self):
        self.frameworks = [
            self.__glib__
        ]

    def __glib__(self, path):
        proportion = -1

        files = utilities.search(
            'glib',
            path, whole=True, include=['*.c*', '*.h*']
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
