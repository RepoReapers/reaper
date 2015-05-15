from lib import utilities

"""
The documentation attribute measures the ratio of comment lines of code to
non-blank lines of code (sloc + cloc) as determined by the `cloc` tool
(http://cloc.sourceforge.net/). Even though GitHub determines the primary
language of each repository, this module will consider source lines and
comment lines of each language cloc reports. We may need to change this in
the future, as one language may require fewer lines of code to express the
same idea than another language.

Author:
    Steven Kroh skk8768@rit.edu

Updated:
    29 April 2015
"""


def run(project_id, repo_path, cursor, **options):
    # Dictionary of language => metrics dictionary
    util = utilities.get_loc(repo_path)

    sloc = 0
    cloc = 0
    for lang, metrics in util.items():
        sloc += metrics['sloc']
        cloc += metrics['cloc']

    ratio = cloc / (sloc + cloc)

    attr_threshold = options['threshold']
    attr_pass = (ratio >= attr_threshold)

    return (attr_pass, ratio)

if __name__ == '__main__':
    print("Attribute plugins are not meant to be executed directly.")
