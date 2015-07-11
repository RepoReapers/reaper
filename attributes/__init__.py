import os
import sys
import types

sys.path.append(os.path.dirname(os.path.realpath(__file__)))


class Attribute(object):
    def __init__(self, attribute):
        self.name = attribute.get('name', '')
        self.initial = attribute.get('initial', '').lower()
        self.weight = attribute.get('weight', 0.0)
        self.enabled = attribute.get('enabled', True)
        self.essential = attribute.get('essential', False)
        self.persist = attribute.get('persist', True)
        self.dependencies = attribute.get('dependencies', list())
        self.options = attribute.get('options', dict())
        self.reference = __import__(self.name)

    def __getstate__(self):
        state = self.__dict__.copy()
        if isinstance(self.reference, types.ModuleType):
            state['reference'] = self.reference.__name__
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        if isinstance(self.reference, str):
            self.reference = __import__(self.reference)


class Attributes(object):
    def __init__(self, attributes, database, keystring=None):
        self.attributes = None
        self.database = database

        self._parse_attributes(attributes)
        self._parse_keystring(keystring)

    def global_init(self, samples):
        for attribute in self.attributes:
            with self.database.cursor() as cursor:
                attribute.reference.global_init(cursor, samples)

    def run(self, project_id, repository_root):
        invalidated = False
        score = 0
        rresults = dict()

        for attribute in self.attributes:
            with self.database.cursor() as cursor:
                attribute.reference.init(cursor)

            with self.database.cursor() as cursor:
                (bresult, rresult) = attribute.reference.run(
                    project_id, repository_path, cursor, attribute.options
                )

            rrresults[attribute.name] = rresult

            if not bresult and attribute.essential:
                score = 0
                invalidated = True

            if not invalidated:
                score += bresult * attribute.weight

        return (score, rresults)

    def _parse_attributes(self, attributes):
        if attributes:
            self.attributes = list()
            for (identifier, attribute) in enumerate(attributes):
                self.attributes.append(Attribute(attribute))

    def _disable_attributes(self):
        for attribute in self.attributes:
            attribute.enabled = False

    def _disable_persistence(self):
        for attribute in self.attributes:
            attribute.persist = False

    def _parse_keystring(self, keystring):
        if keystring:
            # Clean the slate
            self._disable_attributes()
            self._disable_persistence()

            for key in keystring:
                attribute = next(
                    attribute
                    for attribute in self.attributes
                    if attribute.initial == key.lower()
                )
                attribute.enabled = True
                attribute.persist = key.isupper()
