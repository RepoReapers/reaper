from lib import utilities
from attributes.unit_test.discoverer import TestDiscoverer

LANGUAGE = 'C#'


class CSharpTestDiscoverer(TestDiscoverer):
    def __init__(self):
        self.frameworks = [
            self.__nunit__,
            self.__vs_unit_testing__,
            self.__xunit__,
        ]

    def __nunit__(self, path):
        proportion = None

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

    def __vs_unit_testing__(self, path):
        proportion = None

        files = utilities.search(
            'using Microsoft.VisualStudio.TestTools.UnitTesting;',
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

    def __xunit__(self, path):
        proportion = None

        files = utilities.search(
            'using Xunit;',
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
