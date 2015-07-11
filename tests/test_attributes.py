import json
import numbers
import os
import pickle
import types
import unittest

import database
from attributes import Attributes


class AttributesTestCase(unittest.TestCase):
    def setUp(self):
        path = (
            os.path.join(
                os.path.abspath(
                    os.path.join(
                        os.path.dirname(os.path.realpath(__file__)),
                        os.pardir
                    )
                ),
                'attributes',
                'manifest.json'
            )
        )
        self.raw = None
        with open(path, 'r') as file_:
            self.raw = json.load(file_)['attributes']

    def test_init(self):
        # Arrange
        expected = len(self.raw)

        # Act
        attributes = Attributes(self.raw, database=None)

        # Assert
        self.assertEqual(expected, len(attributes.attributes))
        for attribute in attributes.attributes:
            self.assertNotEqual('', attribute.name)
            self.assertNotEqual('', attribute.initial)
            self.assertIsInstance(attribute.weight, numbers.Number)
            self.assertIsInstance(attribute.enabled, bool)
            self.assertIsInstance(attribute.essential, bool)
            self.assertIsInstance(attribute.persist, bool)
            self.assertIsInstance(attribute.dependencies, list)
            self.assertIsInstance(attribute.options, dict)
            self.assertIsInstance(attribute.reference, types.ModuleType)

    def test_pickling(self):
        # Arrange
        attributes = Attributes(self.raw, database=None)
        expected = len(attributes.attributes)

        # Act
        pickled = pickle.dumps(attributes)
        unpickled = pickle.loads(pickled)

        # Assert
        self.assertIsInstance(unpickled, Attributes)
        self.assertEqual(expected, len(unpickled.attributes))
        for attribute in unpickled.attributes:
            self.assertNotEqual('', attribute.name)
            self.assertNotEqual('', attribute.initial)
            self.assertIsInstance(attribute.weight, numbers.Number)
            self.assertIsInstance(attribute.enabled, bool)
            self.assertIsInstance(attribute.essential, bool)
            self.assertIsInstance(attribute.persist, bool)
            self.assertIsInstance(attribute.dependencies, list)
            self.assertIsInstance(attribute.options, dict)
            self.assertIsInstance(attribute.reference, types.ModuleType)

    def test_keystring(self):
        # Arrange
        keystring = 'DuAlIcH'

        # Act
        attributes = Attributes(self.raw, database=None, keystring=keystring)

        # Assert
        for attribute in attributes.attributes:
            index = str.find(keystring.lower(), attribute.initial)
            if index == -1:
                self.assertFalse(attribute.enabled)
            else:
                self.assertTrue(attribute.enabled)
                if keystring[index].isupper():
                    self.assertTrue(attribute.persist)
                else:
                    self.assertFalse(attribute.persist)
