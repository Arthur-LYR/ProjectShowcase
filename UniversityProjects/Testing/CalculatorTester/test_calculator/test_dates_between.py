import unittest
from app.calculator import *


class TestDatesBetween(unittest.TestCase):
    CALCULATOR = Calculator()

    def test_start_date_greater_than_end_date(self):
        start_date = datetime(2021, 9, 28, 0, 0, 0)
        end_date = datetime(2021, 9, 27, 23, 59, 59)

        expected = []
        actual = self.CALCULATOR.dates_between(start_date, end_date)
        self.assertEqual(expected, actual)

    def test_start_date_equal_end_date(self):
        start_date = datetime(2021, 9, 28, 0, 0, 0)
        end_date = datetime(2021, 9, 28, 0, 0, 0)

        expected = [(datetime(2021, 9, 28, 0, 0, 0), datetime(2021, 9, 28, 0, 0, 0))]
        actual = self.CALCULATOR.dates_between(start_date, end_date)
        self.assertEqual(expected, actual)

    def test_end_date_greater_than_start_date(self):
        start_date = datetime(2008, 1, 1, 14, 2, 0)
        end_date = datetime(2008, 1, 3, 5, 0, 9)

        expected = [(datetime(2008, 1, 1, 14, 2, 0), datetime(2008, 1, 2, 0, 0, 0)), (datetime(2008, 1, 2, 0, 0, 0), datetime(2008, 1, 3, 0, 0, 0)), (datetime(2008, 1, 3, 0, 0, 0), datetime(2008, 1, 3, 5, 0, 9))]
        actual = self.CALCULATOR.dates_between(start_date, end_date)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
