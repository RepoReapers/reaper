import os


class CiDiscoverer(object):
    """Base class for all CiDiscoverer classes"""
    def __init__(self):
        self.services = [
            self.__travis__,
            self.__appveyor__,
            self.__circleci__
        ]

    def discover(self, path):
        if not self.services:
            raise Exception('No CI services configured.')

        for service in self.services:
            if service(path):
                return True

        return False

    def __travis__(self, path):
        config = os.path.join(path, '.travis.yml')

        if os.path.exists(config) and os.path.getsize(config) > 0:
            return True

        return False

    def __appveyor__(self, path):
        config = os.path.join(path, 'appveyor.yml')

        if os.path.exists(config) and os.path.getsize(config) > 0:
            return True

        return False

    def __circleci__(self, path):
        config = os.path.join(path, 'circle.yml')

        if os.path.exists(config) and os.path.getsize(config) > 0:
            return True

        return False
