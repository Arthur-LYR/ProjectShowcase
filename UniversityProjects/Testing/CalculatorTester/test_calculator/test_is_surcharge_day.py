import unittest
from app.calculator import *


class TestIsSurchargeDay(unittest.TestCase):
    CALCULATOR = Calculator()

    # AU Holiday on Saturday
    def test_case1(self):
        date = datetime(2021, 12, 25)

        expected = True
        actual = self.CALCULATOR.is_surcharge_day(date)
        self.assertEqual(expected, actual)

    # Not AU Holiday on Saturday
    def test_case2(self):
        date = datetime(2019, 2, 9)

        expected = False
        actual = self.CALCULATOR.is_surcharge_day(date)
        self.assertEqual(expected, actual)

    # Not AU Holiday on Sunday
    def test_case3(self):
        date = datetime(2027, 3, 21)

        expected = False
        actual = self.CALCULATOR.is_surcharge_day(date)
        self.assertEqual(expected, actual)

    # Not AU Holiday on weekend
    def test_case4(self):
        date = datetime(1970, 4, 9)

        expected = True
        actual = self.CALCULATOR.is_surcharge_day(date)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
