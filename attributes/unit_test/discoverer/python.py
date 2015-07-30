from lib import utilities
from attributes.unit_test.discoverer import TestDiscoverer

LANGUAGE = 'Python'


class PythonTestDiscoverer(TestDiscoverer):
    def __init__(self):
        self.frameworks = [
            self.__django_test__,
            self.__nose__,
            self.__unittest__,
        ]

    def __django_test__(self, path):
        proportion = None

        files = utilities.search(
            '((from|import)(\s)(django\.test))',
            path, include=['*.py']
        )

        if files:
            # SLOC of source code
            sloc_code = utilities.get_loc(path)

            # SLOC of test code
            sloc_test = utilities.get_loc(path, files=files)

            if LANGUAGE in sloc_code and LANGUAGE in sloc_test:
                proportion = (
                    sloc_test[LANGUAGE]['sloc'] / sloc_code[LANGUAGE]['sloc']
                )

        return proportion

    def __nose__(self, path):
        proportion = None

        files = utilities.search(
            '((from|import)(\s)(nose))',
            path, include=['*.py']
        )

        if files:
            # SLOC of source code
            sloc_code = utilities.get_loc(path)

            # SLOC of test code
            sloc_test = utilities.get_loc(path, files=files)

            if LANGUAGE in sloc_code and LANGUAGE in sloc_test:
                proportion = (
                    sloc_test[LANGUAGE]['sloc'] / sloc_code[LANGUAGE]['sloc']
                )

        return proportion

    def __unittest__(self, path):
        proportion = None

        files = utilities.search(
            '((from|import)(\s)(unittest))',
            path, include=['*.py']
        )

        if files:
            # SLOC of source code
            sloc_code = utilities.get_loc(path)

            # SLOC of test code
            sloc_test = utilities.get_loc(path, files=files)

            if LANGUAGE in sloc_code and LANGUAGE in sloc_test:
                proportion = (
                    sloc_test[LANGUAGE]['sloc'] / sloc_code[LANGUAGE]['sloc']
                )

        return proportion
