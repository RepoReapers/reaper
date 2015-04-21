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
        mod = __import__(module_, None, None, ['__all__'])
        return getattr(mod, class_)()
    else:
        raise Exception('Test discoverer for %s is not defined.' % language)
