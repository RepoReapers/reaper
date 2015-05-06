import os


class CiDiscoverer(object):
    """Base class for all CiDiscoverer classes"""
    def __init__(self):
        self.services = [
            self.__travis__,
            self.__appveyor__,
            self.__magnumci__,
            self.__circleci__,
            self.__houndci__,
            self.__shippable__,
            self.__solanoci__,
            self.__wercker__
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

    def __magnumci__(self, path):
        config = os.path.join(path, '.magnum.yml')

        if os.path.exists(config) and os.path.getsize(config) > 0:
            return True

        return False

    def __circleci__(self, path):
        config = os.path.join(path, 'circle.yml')

        if os.path.exists(config) and os.path.getsize(config) > 0:
            return True

        return False

    def __houndci__(self, path):
        config = os.path.join(path, '.hound.yml')

        if os.path.exists(config) and os.path.getsize(config) > 0:
            return True

        return False

    def __shippable__(self, path):
        config = os.path.join(path, 'shippable.yml')

        if os.path.exists(config) and os.path.getsize(config) > 0:
            return True

        return False

    def __solanoci__(self, path):
        config = os.path.join(path, 'solano.yml')

        if os.path.exists(config) and os.path.getsize(config) > 0:
            return True

        return False

    def __wercker__(self, path):
        config = os.path.join(path, 'wercker.yml')

        if os.path.exists(config) and os.path.getsize(config) > 0:
            return True

        return False
