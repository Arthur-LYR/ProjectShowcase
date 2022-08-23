import unittest
from unittest.mock import Mock
import main
from app.calculator_form import *


class TestValidateBatteryPackCapacity(unittest.TestCase):
    def test_battery_capacity_none(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False
        with main.ev_calculator_app.app_context():
            calculator_form = Calculator_Form()
            mock_field = Mock()
            mock_field.data = None
            with self.assertRaises(ValidationError):
                calculator_form.validate_BatteryPackCapacity(mock_field)

    def test_empty_battery_capacity(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False
        with main.ev_calculator_app.app_context():
            calculator_form = Calculator_Form()
            mock_field = Mock()
            mock_field.data = ''
            with self.assertRaises(ValueError):
                calculator_form.validate_BatteryPackCapacity(mock_field)

    def test_negative_battery_capacity(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False
        with main.ev_calculator_app.app_context():
            calculator_form = Calculator_Form()
            mock_field = Mock()
            mock_field.data = -1
            with self.assertRaises(ValueError):
                calculator_form.validate_BatteryPackCapacity(mock_field)

    def test_normal_condition(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False
        with main.ev_calculator_app.app_context():
            calculator_form = Calculator_Form()
            mock_field = Mock()
            mock_field.data = 1
            calculator_form.validate_BatteryPackCapacity(mock_field)


if __name__ == '__main__':
    unittest.main()
