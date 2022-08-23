import unittest
from app.calculator import *


class TestTimeCalculation(unittest.TestCase):
    CALCULATOR = Calculator()

    def test_assignment_1_provided(self):
        initial_state = "20"
        final_state = "80"
        capacity = "82"
        charger_configuration = "8"

        expected_hour, expected_minute = 0, 8.43
        actual_hour, actual_minute = self.CALCULATOR.time_calculation(initial_state, final_state, capacity,
                                                                      charger_configuration)
        self.assertEqual(expected_hour, actual_hour)
        self.assertAlmostEqual(expected_minute, actual_minute, 2)

    def test_initial_less_than_final_1(self):
        initial_state = "34"
        final_state = "97"
        capacity = "57"
        charger_configuration = "4"

        expected_hour, expected_minute = 3, 15.87
        actual_hour, actual_minute = self.CALCULATOR.time_calculation(initial_state, final_state, capacity,
                                                                      charger_configuration)
        self.assertEqual(expected_hour, actual_hour)
        self.assertAlmostEqual(expected_minute, actual_minute, 2)

    def test_initial_less_than_final_2(self):
        initial_state = "69"
        final_state = "100"
        capacity = "420"
        charger_configuration = "6"

        expected_hour, expected_minute = 3, 37
        actual_hour, actual_minute = self.CALCULATOR.time_calculation(initial_state, final_state, capacity,
                                                                      charger_configuration)
        self.assertEqual(expected_hour, actual_hour)
        self.assertAlmostEqual(expected_minute, actual_minute, 2)

    def test_initial_less_than_final_3(self):
        initial_state = "21"
        final_state = "69"
        capacity = "151"
        charger_configuration = "5"

        expected_hour, expected_minute = 3, 17.67
        actual_hour, actual_minute = self.CALCULATOR.time_calculation(initial_state, final_state, capacity,
                                                                      charger_configuration)
        self.assertEqual(expected_hour, actual_hour)
        self.assertAlmostEqual(expected_minute, actual_minute, 2)

    def test_initial_less_than_final_4(self):
        initial_state = "17"
        final_state = "84"
        capacity = "100"
        charger_configuration = "1"

        expected_hour, expected_minute = 33, 30
        actual_hour, actual_minute = self.CALCULATOR.time_calculation(initial_state, final_state, capacity,
                                                                      charger_configuration)
        self.assertEqual(expected_hour, actual_hour)
        self.assertAlmostEqual(expected_minute, actual_minute, 2)

    def test_initial_less_than_final_5(self):
        initial_state = "12"
        final_state = "95"
        capacity = "100"
        charger_configuration = "3"

        expected_hour, expected_minute = 11, 31.67
        actual_hour, actual_minute = self.CALCULATOR.time_calculation(initial_state, final_state, capacity,
                                                                      charger_configuration)
        self.assertEqual(expected_hour, actual_hour)
        self.assertAlmostEqual(expected_minute, actual_minute, 2)

    def test_initial_less_than_final_6(self):
        initial_state = "0"
        final_state = "100"
        capacity = "75"
        charger_configuration = "8"

        expected_hour, expected_minute = 0, 12.86
        actual_hour, actual_minute = self.CALCULATOR.time_calculation(initial_state, final_state, capacity,
                                                                      charger_configuration)
        self.assertEqual(expected_hour, actual_hour)
        self.assertAlmostEqual(expected_minute, actual_minute, 2)

    def test_initial_equals_final_1(self):
        initial_state = "0"
        final_state = "0"
        capacity = "56"
        charger_configuration = "1"

        expected_hour, expected_minute = 0, 0
        actual_hour, actual_minute = self.CALCULATOR.time_calculation(initial_state, final_state, capacity,
                                                                      charger_configuration)
        self.assertEqual(expected_hour, actual_hour)
        self.assertAlmostEqual(expected_minute, actual_minute, 2)

    def test_initial_equals_final_2(self):
        initial_state = "100"
        final_state = "100"
        capacity = "342234"
        charger_configuration = "2"

        expected_hour, expected_minute = 0, 0
        actual_hour, actual_minute = self.CALCULATOR.time_calculation(initial_state, final_state, capacity,
                                                                      charger_configuration)
        self.assertEqual(expected_hour, actual_hour)
        self.assertAlmostEqual(expected_minute, actual_minute, 2)

    def test_initial_equals_final_3(self):
        initial_state = "30"
        final_state = "30"
        capacity = "1212"
        charger_configuration = "8"

        expected_hour, expected_minute = 0, 0
        actual_hour, actual_minute = self.CALCULATOR.time_calculation(initial_state, final_state, capacity,
                                                                      charger_configuration)
        self.assertEqual(expected_hour, actual_hour)
        self.assertAlmostEqual(expected_minute, actual_minute, 2)


if __name__ == '__main__':
    unittest.main()
