import unittest

from attributes.unit_test.discoverer import get_test_discoverer, TestDiscoverer
from attributes.unit_test.discoverer import (
    c, cpp, csharp, java, javascript, objectivec, php, python, ruby
)


class TestDiscovererTestCase(unittest.TestCase):
    def test_get_test_discoverer(self):
        # Test: Available test discoverers
        self.assertIsInstance(
            get_test_discoverer('C'),
            c.CTestDiscoverer
        )
        self.assertIsInstance(
            get_test_discoverer('C'),
            TestDiscoverer
        )

        self.assertIsInstance(
            get_test_discoverer('C++'),
            cpp.CppTestDiscoverer
        )
        self.assertIsInstance(
            get_test_discoverer('C++'),
            TestDiscoverer
        )

        self.assertIsInstance(
            get_test_discoverer('C#'),
            csharp.CSharpTestDiscoverer
        )
        self.assertIsInstance(
            get_test_discoverer('C#'),
            TestDiscoverer
        )

        self.assertIsInstance(
            get_test_discoverer('Java'),
            java.JavaTestDiscoverer
        )
        self.assertIsInstance(
            get_test_discoverer('Java'),
            TestDiscoverer
        )

        self.assertIsInstance(
            get_test_discoverer('JavaScript'),
            javascript.JavaScriptTestDiscoverer
        )
        self.assertIsInstance(
            get_test_discoverer('JavaScript'),
            TestDiscoverer
        )

        self.assertIsInstance(
            get_test_discoverer('Objective-C'),
            objectivec.ObjectiveCTestDiscoverer
        )
        self.assertIsInstance(
            get_test_discoverer('Objective-C'),
            TestDiscoverer
        )

        self.assertIsInstance(
            get_test_discoverer('PHP'),
            php.PhpTestDiscoverer
        )
        self.assertIsInstance(
            get_test_discoverer('PHP'),
            TestDiscoverer
        )

        self.assertIsInstance(
            get_test_discoverer('Python'),
            python.PythonTestDiscoverer
        )
        self.assertIsInstance(
            get_test_discoverer('Python'),
            TestDiscoverer
        )

        self.assertIsInstance(
            get_test_discoverer('Ruby'),
            ruby.RubyTestDiscoverer
        )
        self.assertIsInstance(
            get_test_discoverer('Ruby'),
            TestDiscoverer
        )

        # Test: Test discoverer cached objects
        self.assertEqual(
            id(get_test_discoverer('Ruby')),
            id(get_test_discoverer('Ruby'))
        )

        # Test: Case insensitivity of language
        self.assertIsInstance(
            get_test_discoverer('pYtHoN'),
            python.PythonTestDiscoverer
        )

        # Test: Unavailable test discoverer
        self.assertRaises(
            Exception, get_test_discoverer, 'Haskell'
        )

    def test_discover(self):
        discoverer = TestDiscoverer()

        # Test: TestDiscoverer.discover is not callable
        self.assertRaises(Exception, discoverer.discover, path='')
