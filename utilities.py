import os
import subprocess


def get_sloc(path, only=None):
    """Return the source-lines-of-code for each language.

    cloc (http://cloc.sourceforge.net/) is used to compute the
    source-lines-of-code and this method merely parses the output from cloc
    to return a Python-friendly data structure.

    Parameters
    ----------
    path : string
        An absolute path to the source code.
    only : string, optional
        The name(s) of director(y/ies) that must only be included when
        counting the source-lines-of-code.

    Returns
    -------
    sloc : dictionary
        Dictionary keyed by language with source-lines-of-code as the value.
    """
    if not (os.path.exists(path) or os.path.isdir(path)):
        raise Exception('%s is an invalid path.' % path)

    sloc = None

    if only:
        command = ['cloc', '.', '--match-d=%s' % only, '--csv']
    else:
        command = ['cloc', '.', '--csv']

    process = subprocess.Popen(
        command, cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    (out, err) = [x.decode() for x in process.communicate()]

    lines = [line for line in out.split('\n') if len(line.strip('\n')) != 0]
    index = -1
    for _index, _line in enumerate(lines):
        if 'files,' in _line:
            index = _index
            break

    if index != -1:
        sloc = dict()
        for _index in range(index + 1, len(lines)):
            components = lines[_index].split(',')
            sloc[components[1]] = int(components[4])

    return sloc
