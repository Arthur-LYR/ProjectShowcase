import unittest
from app.calculator import *


class TestHoursBetween(unittest.TestCase):
    CALCULATOR = Calculator()

    def test_start_date_greater_than_end_date(self):
        start_time = datetime(2019, 1, 1, 0, 0, 0)
        end_time = datetime(2018, 12, 31, 23, 59, 59)

        expected = []
        actual = self.CALCULATOR.hours_between(start_time, end_time)
        self.assertEqual(expected, actual)

    def test_difference_in_minutes(self):
        start_time = datetime(2034, 4, 5, 9, 0, 0)
        end_time = datetime(2034, 4, 5, 9, 8, 0)

        expected = [(datetime(2034, 4, 5, 9, 0, 0), datetime(2034, 4, 5, 9, 8, 0))]
        actual = self.CALCULATOR.hours_between(start_time, end_time)
        self.assertEqual(expected, actual)

    def test_difference_in_hours_and_minutes(self):
        start_time = datetime(2021, 9, 28, 7, 9, 0)
        end_time = datetime(2021, 9, 28, 9, 0, 0)

        expected = [(datetime(2021, 9, 28, 7, 9, 0), datetime(2021, 9, 28, 8, 0, 0)), (datetime(2021, 9, 28, 8, 0, 0), datetime(2021, 9, 28, 9, 0, 0)), (datetime(2021, 9, 28, 9, 0, 0), datetime(2021, 9, 28, 9, 0, 0))]
        actual = self.CALCULATOR.hours_between(start_time, end_time)
        self.assertEqual(expected, actual)

    def test_different_date_same_hour(self):
        start_time = datetime(2021, 9, 28, 0, 0, 0)
        end_time = datetime(2021, 9, 29, 0, 0, 0)

        expected = [(datetime(2021, 9, 28, 0, 0, 0), datetime(2021, 9, 28, 1, 0, 0)),
                    (datetime(2021, 9, 28, 1, 0, 0), datetime(2021, 9, 28, 2, 0, 0)),
                    (datetime(2021, 9, 28, 2, 0, 0), datetime(2021, 9, 28, 3, 0, 0)),
                    (datetime(2021, 9, 28, 3, 0, 0), datetime(2021, 9, 28, 4, 0, 0)),
                    (datetime(2021, 9, 28, 4, 0, 0), datetime(2021, 9, 28, 5, 0, 0)),
                    (datetime(2021, 9, 28, 5, 0, 0), datetime(2021, 9, 28, 6, 0, 0)),
                    (datetime(2021, 9, 28, 6, 0, 0), datetime(2021, 9, 28, 7, 0, 0)),
                    (datetime(2021, 9, 28, 7, 0, 0), datetime(2021, 9, 28, 8, 0, 0)),
                    (datetime(2021, 9, 28, 8, 0, 0), datetime(2021, 9, 28, 9, 0, 0)),
                    (datetime(2021, 9, 28, 9, 0, 0), datetime(2021, 9, 28, 10, 0, 0)),
                    (datetime(2021, 9, 28, 10, 0, 0), datetime(2021, 9, 28, 11, 0, 0)),
                    (datetime(2021, 9, 28, 11, 0, 0), datetime(2021, 9, 28, 12, 0, 0)),
                    (datetime(2021, 9, 28, 12, 0, 0), datetime(2021, 9, 28, 13, 0, 0)),
                    (datetime(2021, 9, 28, 13, 0, 0), datetime(2021, 9, 28, 14, 0, 0)),
                    (datetime(2021, 9, 28, 14, 0, 0), datetime(2021, 9, 28, 15, 0, 0)),
                    (datetime(2021, 9, 28, 15, 0, 0), datetime(2021, 9, 28, 16, 0, 0)),
                    (datetime(2021, 9, 28, 16, 0, 0), datetime(2021, 9, 28, 17, 0, 0)),
                    (datetime(2021, 9, 28, 17, 0, 0), datetime(2021, 9, 28, 18, 0, 0)),
                    (datetime(2021, 9, 28, 18, 0, 0), datetime(2021, 9, 28, 19, 0, 0)),
                    (datetime(2021, 9, 28, 19, 0, 0), datetime(2021, 9, 28, 20, 0, 0)),
                    (datetime(2021, 9, 28, 20, 0, 0), datetime(2021, 9, 28, 21, 0, 0)),
                    (datetime(2021, 9, 28, 21, 0, 0), datetime(2021, 9, 28, 22, 0, 0)),
                    (datetime(2021, 9, 28, 22, 0, 0), datetime(2021, 9, 28, 23, 0, 0)),
                    (datetime(2021, 9, 28, 23, 0, 0), datetime(2021, 9, 29, 0, 0, 0)),
                    (datetime(2021, 9, 29, 0, 0, 0), datetime(2021, 9, 29, 0, 0, 0))]
        actual = self.CALCULATOR.hours_between(start_time, end_time)

    def test_different_date_different_hour(self):
        start_time = datetime(2021, 9, 28, 0, 0, 0)
        end_time = datetime(2021, 9, 29, 1, 0, 0)

        expected = [(datetime(2021, 9, 28, 0, 0, 0), datetime(2021, 9, 28, 1, 0, 0)),
                    (datetime(2021, 9, 28, 1, 0, 0), datetime(2021, 9, 28, 2, 0, 0)),
                    (datetime(2021, 9, 28, 2, 0, 0), datetime(2021, 9, 28, 3, 0, 0)),
                    (datetime(2021, 9, 28, 3, 0, 0), datetime(2021, 9, 28, 4, 0, 0)),
                    (datetime(2021, 9, 28, 4, 0, 0), datetime(2021, 9, 28, 5, 0, 0)),
                    (datetime(2021, 9, 28, 5, 0, 0), datetime(2021, 9, 28, 6, 0, 0)),
                    (datetime(2021, 9, 28, 6, 0, 0), datetime(2021, 9, 28, 7, 0, 0)),
                    (datetime(2021, 9, 28, 7, 0, 0), datetime(2021, 9, 28, 8, 0, 0)),
                    (datetime(2021, 9, 28, 8, 0, 0), datetime(2021, 9, 28, 9, 0, 0)),
                    (datetime(2021, 9, 28, 9, 0, 0), datetime(2021, 9, 28, 10, 0, 0)),
                    (datetime(2021, 9, 28, 10, 0, 0), datetime(2021, 9, 28, 11, 0, 0)),
                    (datetime(2021, 9, 28, 11, 0, 0), datetime(2021, 9, 28, 12, 0, 0)),
                    (datetime(2021, 9, 28, 12, 0, 0), datetime(2021, 9, 28, 13, 0, 0)),
                    (datetime(2021, 9, 28, 13, 0, 0), datetime(2021, 9, 28, 14, 0, 0)),
                    (datetime(2021, 9, 28, 14, 0, 0), datetime(2021, 9, 28, 15, 0, 0)),
                    (datetime(2021, 9, 28, 15, 0, 0), datetime(2021, 9, 28, 16, 0, 0)),
                    (datetime(2021, 9, 28, 16, 0, 0), datetime(2021, 9, 28, 17, 0, 0)),
                    (datetime(2021, 9, 28, 17, 0, 0), datetime(2021, 9, 28, 18, 0, 0)),
                    (datetime(2021, 9, 28, 18, 0, 0), datetime(2021, 9, 28, 19, 0, 0)),
                    (datetime(2021, 9, 28, 19, 0, 0), datetime(2021, 9, 28, 20, 0, 0)),
                    (datetime(2021, 9, 28, 20, 0, 0), datetime(2021, 9, 28, 21, 0, 0)),
                    (datetime(2021, 9, 28, 21, 0, 0), datetime(2021, 9, 28, 22, 0, 0)),
                    (datetime(2021, 9, 28, 22, 0, 0), datetime(2021, 9, 28, 23, 0, 0)),
                    (datetime(2021, 9, 28, 23, 0, 0), datetime(2021, 9, 29, 0, 0, 0)),
                    (datetime(2021, 9, 29, 0, 0, 0), datetime(2021, 9, 29, 1, 0, 0)),
                    (datetime(2021, 9, 29, 1, 0, 0), datetime(2021, 9, 29, 1, 0, 0))]
        actual = self.CALCULATOR.hours_between(start_time, end_time)


if __name__ == '__main__':
    unittest.main()
