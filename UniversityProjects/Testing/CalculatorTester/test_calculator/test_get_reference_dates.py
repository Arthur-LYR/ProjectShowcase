import unittest
from unittest.mock import Mock
from app.calculator import *


class TestGetReferenceDates(unittest.TestCase):
    CALCULATOR = Calculator()

    def test_before_today(self):
        start_date = datetime(2021, 9, 27, 0, 0, 0)
        end_date = datetime(2021, 9, 28, 0, 0, 0)

        datetime_mock = Mock()
        datetime_mock.now.return_value = datetime(2021, 9, 30, 0, 0, 0)

        expected = [(datetime(2021, 9, 27, 0, 0, 0), datetime(2021, 9, 28, 0, 0, 0))]
        actual = self.CALCULATOR.get_reference_dates(start_date, end_date, date_object=datetime_mock)
        self.assertEqual(expected, actual)

    def test_after_today(self):
        start_date = datetime(2021, 9, 28, 0, 0, 0)
        end_date = datetime(2021, 9, 28, 0, 0, 1)

        datetime_mock = Mock()
        datetime_mock.now.return_value = datetime(2021, 9, 30, 0, 0, 0)

        expected = [(datetime(2020, 9, 28, 0, 0, 0), datetime(2020, 9, 28, 0, 0, 1)),
                    (datetime(2019, 9, 28, 0, 0, 0), datetime(2019, 9, 28, 0, 0, 1)),
                    (datetime(2018, 9, 28, 0, 0, 0), datetime(2018, 9, 28, 0, 0, 1))]
        actual = self.CALCULATOR.get_reference_dates(start_date, end_date, date_object=datetime_mock)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
