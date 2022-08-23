import unittest
from app.calculator import *


class TestStrToDatetime(unittest.TestCase):
    CALCULATOR = Calculator()

    # Valid start_date and start_time
    def test_case1(self):
        start_date = "28/9/2021"
        start_time = "17:35"

        expected = datetime(2021, 9, 28, 17, 35, 0)
        actual = self.CALCULATOR.str_to_datetime(start_date, start_time)
        self.assertEqual(expected, actual)

    # Test for Invalid start_date input
    def test_case2(self):
        start_date = "2019-9-10"
        start_time = "18:29"

        with self.assertRaises(AssertionError):
            self.CALCULATOR.str_to_datetime(start_date, start_time)

    # Test for Invalid start_time Input
    def test_case3(self):
        start_date = "10/7/1979"
        start_time = "5:35pm"

        with self.assertRaises(AssertionError):
            self.CALCULATOR.str_to_datetime(start_date, start_time)

    # Test for Invalid start_date and start_time input
    def test_case4(self):
        start_date = "12.5.2034"
        start_time = "12:00 am"

        with self.assertRaises(AssertionError):
            self.CALCULATOR.str_to_datetime(start_date, start_time)

    # Date Day is Invalid (does not exist)
    def test_case5(self):
        start_date = "120/1/2021"
        start_time = "00:00"

        with self.assertRaises(AssertionError):
            self.CALCULATOR.str_to_datetime(start_date, start_time)

    # Date Month is Invalid (does not exist)
    def test_case6(self):
        start_date = "1/1000/2011"
        start_time = "12:00"

        with self.assertRaises(AssertionError):
            self.CALCULATOR.str_to_datetime(start_date, start_time)

    # Date Year is Invalid (does not exist)
    def test_case7(self):
        start_date = "2/2/10000000"
        start_time = "8:59"

        with self.assertRaises(AssertionError):
            self.CALCULATOR.str_to_datetime(start_date, start_time)

    # Time Hour is Invalid (does not exist)
    def test_case8(self):
        start_date = "1/1/2021"
        start_time = "100:0"

        with self.assertRaises(AssertionError):
            self.CALCULATOR.str_to_datetime(start_date, start_time)

    # Time Minute  is Invalid (does not exist)
    def test_case9(self):
        start_date = "25/12/2009"
        start_time = "1:9010"

        with self.assertRaises(AssertionError):
            self.CALCULATOR.str_to_datetime(start_date, start_time)

    # Invalid Date (Not enough Date Parameter)
    def test_case10(self):
        start_date = "1/8"
        start_time = "12:00"

        with self.assertRaises(AssertionError):
            self.CALCULATOR.str_to_datetime(start_date, start_time)

    # Invalid Time (Not enough Time Parameter)
    def test_case11(self):
        start_date = "1/9/1200"
        start_time = "1"

        with self.assertRaises(AssertionError):
            self.CALCULATOR.str_to_datetime(start_date, start_time)


if __name__ == '__main__':
    unittest.main()
