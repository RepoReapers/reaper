import unittest

from lib import dateutil


class RelativeDeltaTestCase(unittest.TestCase):
    def test_lt_negative(self):
        # Arrange
        delta = dateutil.relativedelta(years=1, months=2)
        threshold = dateutil.relativedelta(years=1)
        expected = False

        # Act
        actual = delta < threshold

        # Assert
        self.assertEqual(expected, actual)

        # Arrange
        delta = dateutil.relativedelta(years=1)
        threshold = dateutil.relativedelta(years=1)
        expected = False

        # Act
        actual = delta < threshold

        # Assert
        self.assertEqual(expected, actual)

    def test_lt_positive(self):
        # Arrange
        delta = dateutil.relativedelta(years=1, months=2)
        threshold = dateutil.relativedelta(years=1, months=6)
        expected = True

        # Act
        actual = delta < threshold

        # Assert
        self.assertEqual(expected, actual)

    def test_gt_negative(self):
        # Arrange
        delta = dateutil.relativedelta(years=1, months=2)
        threshold = dateutil.relativedelta(years=1, months=6)
        expected = False

        # Act
        actual = delta > threshold

        # Assert
        self.assertEqual(expected, actual)

        # Arrange
        delta = dateutil.relativedelta(years=1, months=6)
        threshold = dateutil.relativedelta(years=1, months=6)
        expected = False

        # Act
        actual = delta > threshold

        # Assert
        self.assertEqual(expected, actual)

    def test_gt_positive(self):
        # Arrange
        delta = dateutil.relativedelta(years=2)
        threshold = dateutil.relativedelta(years=1, months=6)
        expected = True

        # Act
        actual = delta > threshold

        # Assert
        self.assertEqual(expected, actual)

    def test_le_negative(self):
        # Arrange
        delta = dateutil.relativedelta(years=2)
        threshold = dateutil.relativedelta(years=1, months=6)
        expected = False

        # Act
        actual = delta <= threshold

        # Assert
        self.assertEqual(expected, actual)

    def test_le_positive(self):
        # Arrange
        delta = dateutil.relativedelta(years=1, months=2)
        threshold = dateutil.relativedelta(years=1, months=6)
        expected = True

        # Act
        actual = delta <= threshold

        # Assert
        self.assertEqual(expected, actual)

        # Arrange
        delta = dateutil.relativedelta(years=1, months=6)
        threshold = dateutil.relativedelta(years=1, months=6)
        expected = True

        # Act
        actual = delta <= threshold

        # Assert
        self.assertEqual(expected, actual)

    def test_ge_negative(self):
        # Arrange
        delta = dateutil.relativedelta(years=2)
        threshold = dateutil.relativedelta(years=2, seconds=1)
        expected = False

        # Act
        actual = delta >= threshold

        # Assert
        self.assertEqual(expected, actual)

    def test_ge_positive(self):
        # Arrange
        delta = dateutil.relativedelta(years=1, months=6, seconds=1)
        threshold = dateutil.relativedelta(years=1, months=6)
        expected = True

        # Act
        actual = delta >= threshold

        # Assert
        self.assertEqual(expected, actual)

        # Arrange
        delta = dateutil.relativedelta(years=1, months=6)
        threshold = dateutil.relativedelta(years=1, months=6)
        expected = True

        # Act
        actual = delta >= threshold

        # Assert
        self.assertEqual(expected, actual)

    def test_total_hours(self):
        # Arrange
        delta = dateutil.relativedelta(years=1, months=6)
        expected = 13080

        # Act
        actual = delta.total_hours()

        # Assert
        self.assertEqual(expected, actual)

    def test_total_minutes(self):
        # Arrange
        delta = dateutil.relativedelta(hours=10)
        expected = 600

        # Act
        actual = delta.total_minutes()

        # Assert
        self.assertEqual(expected, actual)

    def test_total_seconds(self):
        # Arrange
        delta = dateutil.relativedelta(hours=10, minutes=10, seconds=1)
        expected = 36601

        # Act
        actual = delta.total_seconds()

        # Assert
        self.assertEqual(expected, actual)
