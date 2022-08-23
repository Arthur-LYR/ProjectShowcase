import unittest
from app.calculator import *


class TestIsPeakHour(unittest.TestCase):
    CALCULATOR = Calculator()

    # Start hour is smaller than lower bound
    def test_case1(self):
        date = datetime(2021, 6, 5, 5, 59, 59)

        expected = False
        actual = self.CALCULATOR.is_peak_hour(date)
        self.assertEqual(expected, actual)

    # Start hour is exactly at the lower bound
    def test_case2(self):
        date = datetime(2003, 12, 1, 6, 0, 0)

        expected = True
        actual = self.CALCULATOR.is_peak_hour(date)
        self.assertEqual(expected, actual)

    # Start hour is exactly at upper bound
    def test_case3(self):
        date = datetime(2034, 11, 7, 17, 59, 59)

        expected = True
        actual = self.CALCULATOR.is_peak_hour(date)
        self.assertEqual(expected, actual)

    # Start hour is greater than upper bound
    def test_case4(self):
        date = datetime(1901, 5, 23, 18, 0, 0)

        expected = False
        actual = self.CALCULATOR.is_peak_hour(date)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
