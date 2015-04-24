import utilities
from attributes.unit_test.discoverer import TestDiscoverer

# TODO: Include header files as well
LANGUAGE = 'C++'


class CppTestDiscoverer(TestDiscoverer):
    def __init__(self):
        self.frameworks = [
            self.__boost__
        ]

    def __boost__(self, path):
        proportion = -1

        files = utilities.search(
            '(BOOST_TEST_ALTERNATIVE_INIT_API|boost/test/unit_test.hpp|'
            'boost/test/included/unit_test.hpp|BOOST_TEST_DYN_LINK)',
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
