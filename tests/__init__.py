import os
import sys

from lib import utilities

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

ASSETS_PATH = os.path.join(os.path.dirname(__file__), 'assets')
REPOS_PATH = os.path.join(ASSETS_PATH, 'repos')


def get_lsloc(path, languages):
    _sloc = utilities.get_loc(path)
    sloc = 0
    for language in languages:
        if language in _sloc:
            sloc += _sloc[language]['sloc']
    return sloc
