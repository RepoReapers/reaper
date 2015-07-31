TEST_DISCOVERERS = {
    'c': (
        'attributes.unit_test.discoverer.c',
        'CTestDiscoverer'
    ),
    'c++': (
        'attributes.unit_test.discoverer.cpp',
        'CppTestDiscoverer'
    ),
    'c#': (
        'attributes.unit_test.discoverer.csharp',
        'CSharpTestDiscoverer'
    ),
    'javascript': (
        'attributes.unit_test.discoverer.javascript',
        'JavaScriptTestDiscoverer'
    ),
    'java': (
        'attributes.unit_test.discoverer.java',
        'JavaTestDiscoverer'
    ),
    'objective-c': (
        'attributes.unit_test.discoverer.objectivec',
        'ObjectiveCTestDiscoverer'
    ),
    'python': (
        'attributes.unit_test.discoverer.python',
        'PythonTestDiscoverer'
    ),
    'php': (
        'attributes.unit_test.discoverer.php',
        'PhpTestDiscoverer'
    ),
    'ruby': (
        'attributes.unit_test.discoverer.ruby',
        'RubyTestDiscoverer'
    )
}

TEST_DISCOVERER_CACHE = dict()


def _load_test_discoverer(module_, class_):
    mod = __import__(module_, None, None, ['__all__'])
    TEST_DISCOVERER_CACHE[class_] = getattr(mod, class_)()


def get_test_discoverer(language):
    """Return an instance of an appropriate test discover.

    Parameters
    ----------
    language : string
        The programming language for which a test discoverer is needed.

    Returns
    -------
    discoverer : *TestDiscoverer
        A reference to a test discoverer appropriate for the programming
        language.
    """
    _language = language.lower()
    if _language in TEST_DISCOVERERS:
        (module_, class_) = TEST_DISCOVERERS[_language]
        if class_ not in TEST_DISCOVERER_CACHE:
            _load_test_discoverer(module_, class_)
        return TEST_DISCOVERER_CACHE[class_]
    else:
        raise Exception('Test discoverer for %s is not defined.' % language)


class TestDiscoverer(object):
    """Base class for all TestDiscoverer classes"""
    def __init__(self):
        self.frameworks = None

    def discover(self, path):
        if not self.frameworks:
            raise Exception('No unit test frameworks configured.')

        for framework in self.frameworks:
            proportion = framework(path)

            if proportion != 0:
                return proportion

        return 0
