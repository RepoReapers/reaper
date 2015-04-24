import os
import sys

from attributes.continuous_integration.discoverer import CiDiscoverer

ci_discoverer = CiDiscoverer()


def run(project_id, repo_path, cursor, **options):
    return ci_discoverer.discover(repo_path)


if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
