import utilities

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

    if util is None:
        return (0, 0)

    lang_tloc = dict()
    tloc = 0 # Total lines of source or comment code, across all languages
    lloc = 0 # Lines of source or comment code, for a particular language

    for lang, metrics in util.items():
        lloc = int(metrics['sloc']) + int(metrics['cloc']) # Always ignore bloc
        lang_tloc[lang] = lloc
        tloc += lloc

    max_lloc = max(lang_tloc.values())
    max_lloc_proportion = float(max_lloc / tloc)

    attr_pass = 1

    return (attr_pass, max_lloc_proportion)

if __name__ == '__main__':
    print("Attribute plugins are not meant to be executed directly.")
