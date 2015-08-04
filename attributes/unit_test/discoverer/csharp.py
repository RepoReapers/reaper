from attributes.unit_test.discoverer import TestDiscoverer


class CSharpTestDiscoverer(TestDiscoverer):
    def __init__(self):
        self.language = 'C#'
        self.languages = ['C#']
        self.extensions = ['*.cs']
        self.frameworks = [
            self.__nunit__,
            self.__vs_unit_testing__,
            self.__xunit__,
        ]

    def __nunit__(self, path, sloc):
        pattern = 'using NUnit.Framework;'
        return self.measure(path, sloc, pattern)

    def __vs_unit_testing__(self, path, sloc):
        pattern = 'using Microsoft.VisualStudio.TestTools.UnitTesting;'
        return self.measure(path, sloc, pattern)

    def __xunit__(self, path, sloc):
        pattern = 'using Xunit;'
        return self.measure(path, sloc, pattern)
