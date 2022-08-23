import unittest
from app.calculator import *


class TestGetPower(unittest.TestCase):
    CALCULATOR = Calculator()

    # Test for Configuration 1
    def test_case1(self):
        charger_configuration = "1"

        expected = 2
        actual = self.CALCULATOR.get_power(charger_configuration)
        self.assertEqual(expected, actual)

    # Test for Configuration 2
    def test_case2(self):
        charger_configuration = "2"

        expected = 3.6
        actual = self.CALCULATOR.get_power(charger_configuration)
        self.assertEqual(expected, actual)

    # Test for Configuration 3
    def test_case3(self):
        charger_configuration = "3"

        expected = 7.2
        actual = self.CALCULATOR.get_power(charger_configuration)
        self.assertEqual(expected, actual)

    # Test for Configuration 4
    def test_case4(self):
        charger_configuration = "4"

        expected = 11
        actual = self.CALCULATOR.get_power(charger_configuration)
        self.assertEqual(expected, actual)

    # Test for Configuration 5
    def test_case5(self):
        charger_configuration = "5"

        expected = 22
        actual = self.CALCULATOR.get_power(charger_configuration)
        self.assertEqual(expected, actual)

    # Test for Configuration 6
    def test_case6(self):
        charger_configuration = "6"

        expected = 36
        actual = self.CALCULATOR.get_power(charger_configuration)
        self.assertEqual(expected, actual)

    # Test for Configuration 7
    def test_case7(self):
        charger_configuration = "7"

        expected = 90
        actual = self.CALCULATOR.get_power(charger_configuration)
        self.assertEqual(expected, actual)

    # Test for Configuration 8
    def test_case8(self):
        charger_configuration = "8"

        expected = 350
        actual = self.CALCULATOR.get_power(charger_configuration)
        self.assertEqual(expected, actual)

    #  Test for not appropriate config
    def test_case9(self):
        charger_configuration = "sdfbh9347g8he4n98cn"

        with self.assertRaises(AssertionError):
            self.CALCULATOR.get_power(charger_configuration)

    #  Test for wrong type config input
    def test_case10(self):
        # int instead of string
        charger_configuration = 1

        with self.assertRaises(AssertionError):
            self.CALCULATOR.get_power(charger_configuration)


if __name__ == '__main__':
    unittest.main()
