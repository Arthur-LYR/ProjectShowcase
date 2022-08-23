import unittest
from app.calculator import *


class TestCostCalculation1(unittest.TestCase):
    CALCULATOR = Calculator()

    def test_no_time(self):
        time = (0, 0)
        start_date = "4/8/2021"
        start_time = "4:01"
        charger_configuration = "5"

        expected = 0
        actual = self.CALCULATOR.cost_calculation_1(time, start_date, start_time, charger_configuration)
        self.assertAlmostEqual(expected, actual, 2)

    def test_single_surcharge_day_peak_hour(self):
        time = (0, 1476/175)
        start_date = "25/12/1970"
        start_time = "8:00"
        charger_configuration = "8"

        expected = 27.06
        actual = self.CALCULATOR.cost_calculation_1(time, start_date, start_time, charger_configuration)
        self.assertAlmostEqual(expected, actual, 2)

    def test_single_non_surcharge_day_peak_hour(self):
        time = (0, 15)
        start_date = "4/6/2022"
        start_time = "15:00"
        charger_configuration = "7"

        expected = 6.75
        actual = self.CALCULATOR.cost_calculation_1(time, start_date, start_time, charger_configuration)
        self.assertAlmostEqual(expected, actual, 2)

    def test_single_surcharge_day_non_peak_hour(self):
        time = (0, 6)
        start_date = "25/12/2023"
        start_time = "18:01"
        charger_configuration = "8"

        expected = round(9.625, 2)
        actual = round(self.CALCULATOR.cost_calculation_1(time, start_date, start_time, charger_configuration), 2)
        self.assertEqual(expected, actual)

    def test_single_non_surcharge_day_non_peak_hour(self):
        time = (0, 10)
        start_date = "26/7/2008"
        start_time = "5:00"
        charger_configuration = "6"

        expected = 0.6
        actual = self.CALCULATOR.cost_calculation_1(time, start_date, start_time, charger_configuration)
        self.assertAlmostEqual(expected, actual, 2)

    def test_multiple_days_and_hours(self):
        time = (2, 0)
        start_date = "1/10/2021"
        start_time = "23:00"
        charger_configuration = "1"

        expected = 0.11
        actual = self.CALCULATOR.cost_calculation_1(time, start_date, start_time, charger_configuration)
        self.assertAlmostEqual(expected, actual, 2)


if __name__ == '__main__':
    unittest.main()
