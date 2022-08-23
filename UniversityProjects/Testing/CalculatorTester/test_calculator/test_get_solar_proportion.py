import unittest
from app.calculator import *
from unittest.mock import Mock
from unittest.mock import PropertyMock

class TestGetSolarProportion(unittest.TestCase):
    CALCULATOR = Calculator()

    # End Hour greater than sunrise
    def test_case1(self):
        start_hour = datetime(2020, 8, 1, 20, 15, 0)
        end_hour = datetime(2020, 8, 1, 7, 2, 0)
        sunrise = datetime(2020, 8, 1, 7, 5, 0)
        sunset = datetime(2020, 8, 1, 17, 41, 0)

        expected = 0
        actual = self.CALCULATOR.get_solar_proportion(start_hour, end_hour, sunrise, sunset)
        self.assertEqual(expected, actual)

    # Start hour greater than sunset time
    def test_case2(self):
        start_hour = datetime(2020, 8, 1, 18, 25, 0)
        end_hour = datetime(2020, 8, 1, 5, 0, 0)
        sunrise = datetime(2020, 8, 1, 7, 5, 0)
        sunset = datetime(2020, 8, 1, 17, 41, 0)

        expected = 0
        actual = self.CALCULATOR.get_solar_proportion(start_hour, end_hour, sunrise, sunset)
        self.assertEqual(expected, actual)

    # Start charging before sun rise and there is solar energy generated
    def test_case3(self):
        start_hour = datetime(2020, 8, 1, 5, 15, 0)
        end_hour = datetime(2020, 8, 1, 10, 30, 0)
        sunrise = datetime(2020, 8, 1, 7, 5, 0)
        sunset = datetime(2020, 8, 1, 17, 41, 0)

        expected = 3.4166666666666665
        actual = self.CALCULATOR.get_solar_proportion(start_hour, end_hour, sunrise, sunset)
        self.assertEqual(expected, actual)

    # The charging done after  sun set but start before sunset so there is solar energy generated
    def test_case4(self):
        start_hour = datetime(2020, 8, 1, 14, 7, 0)
        end_hour = datetime(2020, 8, 1, 18, 15, 0)
        sunrise = datetime(2020, 8, 1, 7, 5, 0)
        sunset = datetime(2020, 8, 1, 17, 41, 0)

        expected = 3.566666666666667
        actual = self.CALCULATOR.get_solar_proportion(start_hour, end_hour, sunrise, sunset)
        self.assertEqual(expected, actual)

    # There is solar energy generated during the whole charging session
    def test_case5(self):
        start_hour = datetime(2020, 8, 1, 10, 45, 0)
        end_hour = datetime(2020, 8, 1, 15, 50, 0)
        sunrise = datetime(2020, 8, 1, 7, 5, 0)
        sunset = datetime(2020, 8, 1, 17, 41, 0)

        expected = 5.083333333333333
        actual = self.CALCULATOR.get_solar_proportion(start_hour, end_hour, sunrise, sunset)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
